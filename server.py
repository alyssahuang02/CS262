import socket
import sys
import selectors
import types

sel = selectors.DefaultSelector()

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

# queue containing all messages; c
# TODO: can we put metadata to indicate who the intended recipient is?
messages = []

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((HOST, PORT))
lsock.listen()
print(f"Listening on {(HOST, PORT)}")
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    # print(f"data addr: {data.addr}")
    # print(f"read condition: {mask & selectors.EVENT_READ}")
    # print(f"write condition: {mask & selectors.EVENT_WRITE}")
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
            print(f"Closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if len(messages) != 0:
            for message in messages:
                print(f"Sending {message} to {data.addr}")
                while len(message) != 0:
                    sent = sock.send(message)
                    message = message[sent:]
        messages.clear()
        if data.outb:
            print(data.outb)
            messages.append(data.outb)

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)

except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()
