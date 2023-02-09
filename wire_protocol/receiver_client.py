import socket
HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65431  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        print("Now listening...\n")
        data = s.recv(1024)
        if not data:
            break
        elif data == 'killsrv':
            s.close()
        else:
            print(data)

    # ## HOW TO KEEP CONNECTION OPEN
    # data = s.recv(1024)
    # # list of array
    # if data == "Send more info":
    #     input("What username do you want?")
    # print("second", data)
    # while data:
    #     print('in while loop Received:' + data.decode())
    #     data = s.recv(1024)

print(f"Received {data!r}")