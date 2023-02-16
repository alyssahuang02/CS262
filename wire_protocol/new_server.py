import socket 
import threading
import re
from commands import *

mutex = threading.Lock() # TODO: THIS STUFF

class ChatServer:
    def __init__(self):
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
        else:
            # Log in user
            mutex.acquire()
            self.active_accounts[username] = addr
            mutex.release()
            logged_in = True
        
        self.send(conn, NOTIFY, LOGIN_SUCCESSFUL)
        return (username, logged_in)

    def register_user(self, conn, username, addr):
        registered = False
        
        print(f"[{addr}] {username}")

        # DO WE NEED A MUTEX HERE???
        if username in self.accounts:
            self.send(conn, NOTIFY, "Username already exists.")
        else:
            # Register and log in user
            mutex.acquire()
            self.active_accounts[username] = addr
            self.accounts.append(username)
            self.unsent_messages[username] = []
            mutex.release()
            registered = True
        
        self.send(conn, NOTIFY, "Login successful!")
        return (username, registered)

    # Precondition: recipient is in list of accounts
    def record_chat_message(self, conn, sender, recipient, msg):
        mutex.acquire()
        self.unsent_messages[recipient].append((sender, msg))
        mutex.release()
        self.send(conn, NOTIFY, "Message sent!")
    

    # Sends all unsent messages to the user who is currently connected at given address
    def send_unsent_messages(self, conn, addr):
        mutex.acquire()
        for recipient in self.unsent_messages:
            messages = self.unsent_messages[recipient]

            if recipient in self.active_accounts:
                recipient_addr = self.active_accounts[recipient]
                if recipient_addr == addr:
                    for message in messages:
                        text = message[0] + " sends: " + message[1]
                        self.send(conn, NOTIFY, text)
                    
            # TODO: do this in a thread-safe way lmao
            # TODO: Need to modify this to delete stuff
            # WHAT IF THE RECIPIENT DISCONNECTS?
            self.unsent_messages[recipient] = []
        mutex.release()
        self.send(conn, NO_MORE_DATA, " ")

    # Precondition: we have already checked that the username corresponds to
    # the user who was logged in at the time
    def delete_account(self, conn, username):
        mutex.acquire()
        del self.active_accounts[username]
        del self.unsent_messages[username]
        self.accounts.remove(username)
        mutex.release()
        self.send(conn, NOTIFY, DELETION_SUCCESSFUL)
    

    # Precondition: we have already checked that the username corresponds to
    # the user who was logged in at the time
    def logout(self, conn, username):
        mutex.acquire()
        del self.active_accounts[username]
        mutex.release()
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

                # Checks that the user currently logged in is the one who is trying to delete their account
                for user in self.active_accounts:
                    if user == username and self.active_accounts[user] == addr:
                        self.delete_account(conn, username)
                        continue
                self.send(conn, NOTIFY, "You cannot another user's account.")
                continue
            
            elif purpose == SHOW_ACCOUNTS:
                username = parsed_message[BODY]
                matched_accounts = []
            
                mutex.acquire()
                for account in self.accounts:
                    x = re.search(username, account)
                    if x is not None:
                        matched_accounts.append(account)
                mutex.release()
                if len(matched_accounts) == 0:
                    self.send(conn, NOTIFY, USER_DOES_NOT_EXIST)
                else:
                    # might throw an error with lists
                    self.send(conn, NOTIFY, matched_accounts)


        
        
        
        # connected = True
        # while connected:
        #     # depends on your protocol
        #     msg_length = conn.recv(HEADER).decode(FORMAT)
        #     if msg_length:
        #         msg_length = int(msg_length)
        #         msg = conn.recv(msg_length).decode(FORMAT)
        #         if msg == DISCONNECT_MESSAGE:
        #             connected = False
        #         print(f"[{addr}] {msg}")
        #         conn.send("Msg received".encode(FORMAT))

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


    # Return a dictionary representation of the message
    def receive(self, conn):
        try:
            full_message = conn.recv(MAX_BANDWIDTH).decode(FORMAT)
        except:
            raise ValueError
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

        
    # Notes: new thread for each client! (do we have to log them out?)
    def start(self):
        self.server.listen()
        print(f"[LISTENING] Server is listening on {SERVER}")
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

chat_server = ChatServer()
print("[STARTING] server is starting...")
chat_server.start()