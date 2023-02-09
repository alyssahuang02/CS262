import socket

# TODO: MAKE SURE THEY USE PYTHON 3 OR HIGHER

# HOST = "127.0.0.1"  # The server's hostname or IP address
# PORT = 65431  # The port used by the server

# # messages = [b"Hello world", b"Morning world", b"Goodnight world", b"Goodbye world"]
# messages = [b"Hello world"]

# for message in messages:
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.connect((HOST, PORT))
#         # TODO: Specify which client to send to
#         s.sendall(message)

# print("messages sent!")

HOST = None
PORT = None

SOCKET = None

MAX_MESSAGE_LENGTH = 1000
MAX_USERNAME_LENGTH = 24

def connection_prompt():
    host = input("Enter the host IP address: ")
    print(host)
    port = input("Enter the port number: ")

    if not port.isdigit():
        print("Invalid port. Please try again.")
        connection_prompt()
    
    port = int(port)
    if port < 0:
        print("Invalid port. Please try again.")
        connection_prompt()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try: 
        s.connect((host, port))
    except:
        print("Invalid host/port. Please try again.")
        connection_prompt()
    
    HOST=host
    PORT=port
    SOCKET=s

def check_username(username):
    pass

def send_message():
    recipient = input("Enter the recipient: ")
    if not check_username(recipient):
        raise Exception("Invalid username. Please try again.")

    message = input("Enter a message to send: ")
    # TODO: i dont think this is the right bit/byte conversion but check later
    if len(message) > MAX_MESSAGE_LENGTH:
        raise Exception("Message too long. Max length is " + MAX_MESSAGE_LENGTH + " characters.")
    
    buffer = bytearray(1024)
    message = bytes(message, "utf-8") # TODO: check this

    SOCKET.sendall(buffer)

def main():
    # connection_prompt()
    send_message()