import socket 
import threading
import pickle

# bytes for the metadata of how long the message is, then cater the actual size
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# before we queue it onto the message 
messages = []
accounts = {}

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    logged_in = False
    current_user = None

    # establish username
    while not logged_in:
        conn.send("What's your username?".encode(FORMAT))
        msg_length = conn.recv(HEADER).decode(FORMAT)
        msg_length = int(msg_length)
        username = conn.recv(msg_length).decode(FORMAT)
        
        print(f"[{addr}] {username}")

        if username in accounts.keys():
            conn.send("Username already exists. What's your username?".encode(FORMAT))
            print("username already exists")
        else:
            accounts[username] = addr
            current_user = username
            logged_in = True
            conn.send("Logged in!".encode(FORMAT))


    # send current users
    print("current users")

    data_string = pickle.dumps(list(accounts.keys()))
    conn.send(data_string)


    connected = True
    while connected:
        # depends on your protocol
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))

    conn.close()
        

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()