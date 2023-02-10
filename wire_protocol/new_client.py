import socket
import pickle

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "10.250.18.31"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    
    data = client.recv(2048).decode(FORMAT)
    print(data)
    return data

logged_in = False
start = client.recv(2048).decode(FORMAT)
print("start", start)

if start == "What's your username?":
    while not logged_in:
        username = input()
        data = send(username)

        if data == "Logged in!":
            logged_in = True


users = client.recv(2048)
users_arr = pickle.loads(users)
print(users_arr)

# send a message - maybe commands of who to send a message to

# print("continue")
# # receive 
# data = client.recv(2048)
# data_arr = pickle.loads(data)

# send("Hello World!")
# input()
# send("Hello Everyone!")
# input()
# send("Hello Tim!")

# send(DISCONNECT_MESSAGE)