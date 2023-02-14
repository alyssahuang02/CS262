import socket 
import threading
import pickle

# bytes for the metadata of how long the message is, then cater the actual size
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname()) # TODO: WHAT IS THIS?
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
PULL_MESSAGE = "!PULL"
SEND_MESSAGE = "!SEND"
LOGIN = "!LOGIN"
REGISTER = "!REGISTER"
PURPOSE = "!PURPOSE:"
RECIPIENT = "!RECIPIENT:"
SENDER = "!SENDER:"
LENGTH = "!LENGTH:"
BODY = "!BODY:"
SEPARATOR = "/"
MAX_BANDWIDTH = 2048

# Server stuff
NOTIFY = "!NOTIFY" # you have to always print out the body if purpose is notify
# server already preprocesses the message to be received
NO_MORE_DATA = "!NOMOREDATA"

class ChatServer:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDR)

        # TODO: will need to use a mutex lock for each of these likely
        self.unsent_messages = {} # {username: [msg1, msg2, msg3]}
        self.accounts = [] # [username1, username2, username3]
        self.active_accounts = {} # {username: addr}

    def login_user(self, conn, addr):
        logged_in = False
        # self.send("What's your username?", conn)
        username = self.receive(conn)
        
        print(f"[{addr}] {username}")

        if username not in self.accounts:
            self.send("Username does not exist.", conn)
        else:
            # Log in user
            self.active_accounts[username] = addr
            logged_in = True
        
        self.send(NOTIFY, "Login successful!")
        return (username, logged_in)

    def register_user(self, conn, addr):
        registered = False
        self.send("What's your username?", conn)
        username = self.receive(conn)
        
        print(f"[{addr}] {username}")

        if username in self.accounts:
            self.send("Username already exists.", conn)
        else:
            # Register and log in user
            self.active_accounts[username] = addr
            self.accounts.append(username)
            self.unsent_messages[username] = []
            registered = True
        
        self.send(NOTIFY, "Login successful!")
        return (username, registered)

    def record_chat_message(self, conn, addr):
        # Block until we get the sender's username
        sender = self.receive(conn)

        # TODO: we should lowkey wrap this in a function LOL
        self.send("Who do you want to send a message to?", conn)
        recipient = self.receive(conn)

        if recipient not in self.accounts:
            self.send("User does not exist.", conn)
            # TODO: handle error better lolz
            return
        
        self.send("What's your message?", conn)
        msg = self.receive(conn)

        self.unsent_messages[recipient].append((sender, msg))

        self.send(NOTIFY, "Message sent!")
    

    # Sends all unsent messages to the user who is currently connected at given address
    def send_unsent_messages(self, conn, addr):
        for recipient in self.unsent_messages:
            messages = self.unsent_messages[recipient]

            if recipient in self.active_accounts:
                recipient_addr = self.active_accounts[recipient]
                if recipient_addr == addr:
                    for message in messages:
                        text = message[0] + " sends: " + message[1]
                        self.send(SEND_MESSAGE, text)
                    
            # TODO: do this in a thread-safe way lmao
            # TODO: Need to modify this to delete stuff
            # self.unsent_messages[recipient] = []
        self.send(NO_MORE_DATA, "")

    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        logged_in = False

        # while not disconnected
        while True:
            parsed_message = self.receive(conn)

            purpose = parsed_message[PURPOSE]
            if purpose == LOGIN:
                username, logged_in = self.login_user(conn, addr)
            elif purpose == REGISTER:
                username, logged_in = self.register_user(conn, addr)
            elif purpose == SEND_MESSAGE:
                if not logged_in:
                    self.send(NOTIFY, "You must be logged in to send a message.")
                    continue
                self.record_chat_message(conn, addr)
            elif purpose == PULL_MESSAGE:
                if not logged_in:
                    self.send(NOTIFY, "You must be logged in to receive messages.")
                    continue
                self.send_unsent_messages(conn, addr)


        # TODO: we have to make this a background process somehow later??
        

        # TODO: add here i forgot the specs
        # conn.send("Enter 0 to send a message. Enter 1 to delete account.".encode(FORMAT))

        # msg_length = conn.recv(HEADER).decode(FORMAT)
        # if msg_length:
        #     msg_length = int(msg_length)
        #     action = conn.recv(msg_length).decode(FORMAT)
        
        
        
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
        data=PURPOSE + purpose
        if recipient and sender:
            data += SEPARATOR + RECIPIENT + recipient
            data += SEPARATOR + SENDER + sender
        if body:
            length = len(body)
            data+= SEPARATOR + LENGTH + length
            data+= SEPARATOR + BODY + body
        return data
    
    
    def send(self, purpose, body, recipient=None, sender=None):
        msg = self.create_message(purpose, body, recipient, sender)
        try:
            self.client.send(msg.encode(FORMAT))
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
        for i in range(len(split_message)):
            part = split_message[i]
            if part != BODY:
                parsed_message[part] = split_message[i+1]
                i += 1
            else:
                body = split_message[i+1:].join("/")
                length = int(parsed_message[LENGTH])
                parsed_message[part] = body[:length]
                break
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