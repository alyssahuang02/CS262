import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65431  # The port used by the server

# messages = [b"Hello world", b"Morning world", b"Goodnight world", b"Goodbye world"]
messages = [b"Hello world"]

for message in messages:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        # TODO: Specify which client to send to
        s.sendall(message)

print("messages sent!")
