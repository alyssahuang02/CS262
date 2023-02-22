import socket 
import threading
import re
from commands import *

mutex_unsent_messages = threading.Lock()
mutex_accounts = threading.Lock()
mutex_active_accounts = threading.Lock()

class ChatServer:
    def __init__(self, test=False):
        if not test:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind(ADDR)

        # TODO: will need to use a mutex lock for each of these likely
        self.unsent_messages = {} # {username: [msg1, msg2, msg3]}
        self.accounts = [] # [username1, username2, username3]
        self.active_accounts = {} # {username: addr}

    def login_user(self, conn, username, addr):
        logged_in = False
        
        print(f"[{addr}] {username}")

        if username not in self.accounts:
            self.send(conn, NOTIFY, "Username does not exist.")
            return (None, None)
        
        # Checks if user is logged in already
        if username in self.active_accounts:
            self.send(conn, NOTIFY, "User is already logged in.")
            return (None, None)

        # Log in user
        mutex_active_accounts.acquire()
        self.active_accounts[username] = addr
        mutex_active_accounts.release()

        logged_in = True
        
        self.send(conn, NOTIFY, LOGIN_SUCCESSFUL)
        return (username, logged_in)

    def register_user(self, conn, username, addr):
        registered = False
        
        print(f"[{addr}] {username}")

        # DO WE NEED A MUTEX HERE???
        if username in self.accounts:
            self.send(conn, NOTIFY, "Username already exists.")
            return (None, None)
        # Register and log in user

        # TODO: check if these mutices are in correct order
        mutex_active_accounts.acquire()
        self.active_accounts[username] = addr
        mutex_active_accounts.release()

        mutex_accounts.acquire()
        self.accounts.append(username)
        mutex_accounts.release()

        mutex_unsent_messages.acquire()
        self.unsent_messages[username] = []
        mutex_unsent_messages.release()

        registered = True

        self.send(conn, NOTIFY, LOGIN_SUCCESSFUL)
        return (username, registered)

    # Precondition: recipient is in list of accounts
    def record_chat_message(self, conn, sender, recipient, msg):
        mutex_unsent_messages.acquire()
        self.unsent_messages[recipient].append((sender, msg))
        mutex_unsent_messages.release()
        self.send(conn, NOTIFY, "Message sent!")
    

    # Sends all unsent messages to the user who is currently connected at given address
    def send_unsent_messages(self, conn, addr):
        for recipient in self.unsent_messages:
            messages = self.unsent_messages[recipient]

            if recipient in self.active_accounts:
                recipient_addr = self.active_accounts[recipient]
                if recipient_addr == addr:
                    print("waiting for mutex")
                    mutex_unsent_messages.acquire()
                    print("got mutex")
                    for message in messages:
                        text = message[0] + " sends: " + message[1]
                        self.send(conn, NOTIFY, text)
                    self.unsent_messages[recipient] = []
                    print("mutex released")
                    mutex_unsent_messages.release()

                    # Assumes user is only logged into one terminal
                    self.send(conn, NO_MORE_DATA, " ")

    # Precondition: we have already checked that the username corresponds to
    # the user who was logged in at the time
    def delete_account(self, conn, username):
        mutex_active_accounts.acquire()
        del self.active_accounts[username]
        mutex_active_accounts.release()

        mutex_unsent_messages.acquire()
        del self.unsent_messages[username]
        mutex_unsent_messages.release()

        mutex_accounts.acquire()
        self.accounts.remove(username)
        mutex_accounts.release()

        self.send(conn, NOTIFY, DELETION_SUCCESSFUL)
    

    # Precondition: we have already checked that the username corresponds to
    # the user who was logged in at the time
    def logout(self, conn, username):

        mutex_active_accounts.acquire()
        del self.active_accounts[username]
        mutex_active_accounts.release()

        self.send(conn, NOTIFY, LOGOUT_SUCCESSFUL)
    

    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        logged_in = False

        # while not disconnected
        while True:
            parsed_message = self.receive(conn)

            print(parsed_message)
            purpose = parsed_message[PURPOSE]
            if purpose == LOGIN:
                username = parsed_message[BODY]
                username, logged_in = self.login_user(conn, username, addr)
            elif purpose == REGISTER:
                username = parsed_message[BODY]
                username, logged_in = self.register_user(conn, username, addr)
            elif purpose == SEND_MESSAGE:
                if not logged_in:
                    self.send(conn, NOTIFY, "You must be logged in to send a message.")
                    continue
                sender = parsed_message[SENDER]
                recipient = parsed_message[RECIPIENT]
                msg = parsed_message[BODY]
                self.record_chat_message(conn, sender, recipient, msg)
            elif purpose == PULL_MESSAGE:
                if not logged_in:
                    self.send(conn, NOTIFY, "You must be logged in to receive messages.")
                    continue

                self.send_unsent_messages(conn, addr)
            elif purpose == CHECK_USER_EXISTS:
                username = parsed_message[BODY]
                if username in self.accounts:
                    self.send(conn, NOTIFY, "User exists.")
                else:
                    self.send(conn, NOTIFY, USER_DOES_NOT_EXIST)
            
            elif purpose == DELETE_ACCOUNT:
                if not logged_in:
                    self.send(conn, NOTIFY, "You must be logged in to delete an account.")
                    continue
                username = parsed_message[BODY]

                self.delete_account(conn, username)
            
            elif purpose == SHOW_ACCOUNTS:
                username = parsed_message[BODY]
                matched_accounts = "\nUsers:\n"
                no_accounts_found_length = len(matched_accounts)
            
                for account in self.accounts:
                    # I think this regex looks for anything that has that username thingy in it
                    # x = re.search(username, account)
                    # if x is not None:

                    if account.startswith(username):
                        matched_accounts += account + "\n"
                if len(matched_accounts) == no_accounts_found_length:
                    self.send(conn, NOTIFY, USER_DOES_NOT_EXIST)
                else:
                    self.send(conn, NOTIFY, matched_accounts)

            elif purpose == LOGOUT:
                if not logged_in:
                    self.send(conn, NOTIFY, "You must be logged in to log out.")
                    continue

                username = parsed_message[BODY]
                self.logout(conn, username)
                logged_in = False

        conn.close()


    def create_message(self, purpose, body, recipient=None, sender=None):
        data=PURPOSE + SEPARATOR + purpose
        if recipient and sender:
            data += SEPARATOR + RECIPIENT + SEPARATOR + recipient
            data += SEPARATOR + SENDER + SEPARATOR + sender
        if body:
            length = len(body)
            data += SEPARATOR + LENGTH + SEPARATOR + str(length)
            data += SEPARATOR + BODY + SEPARATOR + body
        
        return data
    
    
    def send(self, conn, purpose, body, recipient=None, sender=None):
        msg = self.create_message(purpose, body, recipient, sender)
        print(msg)
        try:
            conn.send(msg.encode(FORMAT))
        except:
            raise ValueError


    def parse_message(self, full_message):
        split_message = full_message.split("/")
        parsed_message = {}
        i = 0
        while i < len(split_message):
            part = split_message[i]
            if BODY != part:
                parsed_message[part] = split_message[i+1]
                i += 1
            else:
                body = "/".join(split_message[i+1:])
                length = int(parsed_message[LENGTH])
                parsed_message[part] = body[:length]
                break
            i += 1
        return parsed_message
    

    # Return a dictionary representation of the message
    def receive(self, conn):
        try:
            full_message = conn.recv(MAX_BANDWIDTH).decode(FORMAT)
        except:
            raise ValueError
        
        return self.parse_message(full_message)

        
    # Notes: new thread for each client! (do we have to log them out?)
    def start(self):
        self.server.listen()
        print(f"[LISTENING] Server is listening on {SERVER}")
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")