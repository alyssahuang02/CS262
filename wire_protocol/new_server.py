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
LOGIN_SUCCESS = "!LOGGEDIN"
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
        self.send("What's your username?".encode(FORMAT), conn)
        username = self.receive(conn)
        
        print(f"[{addr}] {username}")

        if username not in self.accounts:
            self.send("Username does not exist.", conn)
        else:
            # Log in user
            self.active_accounts[username] = addr
        
        return username

    def register_user(self, conn, addr):
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
        
        return username

    def record_chat_message(self, conn, addr):
        # Block until we get the sender's username
        sender = self.receive(conn)

        print(sender)

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
    
    def send_unsent_messages(self, conn, addr):
        for recipient in self.unsent_messages:
            messages = self.unsent_messages[recipient]
            print(messages)
            for message in messages:
                if recipient in self.active_accounts:
                    recipient_addr = self.active_accounts[recipient]
                    if recipient_addr == addr:
                        # Are currently in the thread that is the recipient's connection
                        text = message[0] + " sends: " + message[1]
                        self.send(text, conn)
                        # TODO: confirm message has been received
            # TODO: do this in a thread-safe way lmao
            self.unsent_messages[recipient] = []
        self.send(NO_MORE_DATA, conn)

    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        logged_in = False

        # establish username
        while not logged_in:
            self.send("Enter 0 to register. Enter 1 to login.", conn)
            # conn.send("Enter 0 to register. Enter 1 to login.".encode(FORMAT))

            # msg_length = conn.recv(HEADER).decode(FORMAT)
            # if msg_length:
            #     msg_length = int(msg_length)
            #     action = conn.recv(msg_length).decode(FORMAT)

            action = self.receive(conn)
            print(action)
            print("action received")

            if action == "0":
                print("the user selected 0")
                username = self.register_user(conn, addr)
                logged_in = True
            elif action == "1":
                username = self.login_user(conn, addr)
                logged_in = True
            else:
                self.send("Invalid input.", conn)
                # TODO: CHANGE THIS TO WHILE LOOP LATER LOL

        # TODO: some protocol for all this shit
        self.send(LOGIN_SUCCESS, conn)

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
            
    def send(self, msg, conn):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        conn.send(send_length)
        conn.send(message)

    def receive(self, conn):
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            action = conn.recv(msg_length).decode(FORMAT)

            return action
        else:
            return "ERROR"

        
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