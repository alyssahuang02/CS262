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
LOGIN_MESSAGE = "!LOGGEDIN"
NO_MORE_DATA = "!NOMOREDATA"
SPLIT_MESSAGE = "#" # need to change this

class ChatServer:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDR)

        # TODO: will need to use a mutex lock for each of these likely
        self.unsent_messages = {} # {username: [msg1, msg2, msg3]}
        self.accounts = [] # [username1, username2, username3]
        self.active_accounts = {} # {username: addr}

    def login_user(self, conn, addr):
        conn.send("What's your username?".encode(FORMAT))
        msg_length = conn.recv(HEADER).decode(FORMAT)
        msg_length = int(msg_length)
        username = conn.recv(msg_length).decode(FORMAT)
        
        print(f"[{addr}] {username}")

        if username not in self.accounts:
            conn.send("Username does not exist.".encode(FORMAT))
        else:
            # Log in user
            self.active_accounts[username] = addr
        
        return username

    def register_user(self, conn, addr):
        conn.send("What's your username?".encode(FORMAT))
        msg_length = conn.recv(HEADER).decode(FORMAT)
        msg_length = int(msg_length)
        username = conn.recv(msg_length).decode(FORMAT)
        
        print(f"[{addr}] {username}")

        if username in self.accounts:
            conn.send("Username already exists.".encode(FORMAT))
        else:
            # Register and log in user
            self.active_accounts[username] = addr
            self.accounts.append(username)
            self.unsent_messages[username] = []
        
        return username

    def record_chat_message(self, conn, addr):
        # Block until we get the sender's username
        sender = conn.recv(2048).decode(FORMAT)

        print(sender)

        # TODO: we should lowkey wrap this in a function LOL
        conn.send("Who do you want to send a message to?".encode(FORMAT))
        msg_length = conn.recv(HEADER).decode(FORMAT)
        msg_length = int(msg_length)
        recipient = conn.recv(msg_length).decode(FORMAT)

        if recipient not in self.accounts:
            conn.send("User does not exist.".encode(FORMAT))
            # TODO: handle error better lolz
            return
        
        conn.send("What's your message?".encode(FORMAT))
        msg_length = conn.recv(HEADER).decode(FORMAT)
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)

        self.unsent_messages[recipient].append((sender, msg))
    
    def send_unsent_messages(self, conn, addr):
        for recipient in self.unsent_messages:
            messages = self.unsent_messages[recipient]
            print(messages)
            for message in messages:
                if recipient in self.active_accounts:
                    recipient_addr = self.active_accounts[recipient]
                    if recipient_addr == addr:
                        # Are currently in the thread that is the recipient's connection
                        conn.send(message[0].encode(FORMAT))
                        conn.send(" sends: ".encode(FORMAT))
                        conn.send(message[1].encode(FORMAT))
                        # TODO: confirm message has been received
            # TODO: do this in a thread-safe way lmao
            self.unsent_messages[recipient] = []
        conn.send(NO_MORE_DATA.encode(FORMAT))

    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        logged_in = False

        # establish username
        if not logged_in:
            conn.send("Enter 0 to register. Enter 1 to login.".encode(FORMAT))

            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                action = conn.recv(msg_length).decode(FORMAT)

            print(action)

            if action == "0":
                username = self.register_user(conn, addr)
            elif action == "1":
                username = self.login_user(conn, addr)
            else:
                conn.send("Invalid input.".encode(FORMAT))
                # TODO: CHANGE THIS TO WHILE LOOP LATER LOL

        # TODO: some protocol for all this shit
        conn.send(LOGIN_MESSAGE.encode(FORMAT))

        # TODO: we have to make this a background process somehow later??
        self.send_unsent_messages(conn, addr)

        # TODO: add here i forgot the specs
        # conn.send("Enter 0 to send a message. Enter 1 to delete account.".encode(FORMAT))

        # msg_length = conn.recv(HEADER).decode(FORMAT)
        # if msg_length:
        #     msg_length = int(msg_length)
        #     action = conn.recv(msg_length).decode(FORMAT)
        
        self.record_chat_message(conn, addr)
        
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