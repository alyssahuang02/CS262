import socket
import pickle # we can't use this in our final implementation according to waldo

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "10.250.10.42" # TODO: need to change later/have some way to make it dynamic
ADDR = (SERVER, PORT)
LOGIN_MESSAGE = "!LOGGEDIN"
NO_MORE_DATA = "!NOMOREDATA"

class ChatClient:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)

        self.logged_in = False
        self.username = None

        while not self.logged_in:
            # TODO: ensure that blocking happens here; fine cuz we have sep thread for each client
            response = self.wait_for_response()
            print(response)

            # First sends a confirmation that the user has logged in, then the username
            if LOGIN_MESSAGE in response:
                # TODO: ITS SENDING LIKE 3 things at once need to figure that shit out
                # TODO: partiion messages?
                self.logged_in = True
                print("Logged in!")
                self.username = user_input
                break
            
            user_input = input()
            self.send(user_input)
        
        # Receive all missed messages
        while NO_MORE_DATA not in response:
            print(response)
            response = self.wait_for_response()
        
        print("No more messages.")
        # Client decides what to do after logging in
        # print(self.wait_for_response())
        # action = input()
        # self.send(action)
        # print(action)
        # if action == "0":
        
        # TODO: literally zero error handling
        self.send(self.username)

        prompt = self.wait_for_response()
        print(prompt)

        recipient = input()
        self.send(recipient)

        prompt = self.wait_for_response()
        print(prompt)

        message = input()
        self.send(message)

        print("Message sent!")

    def send(self, msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)
    
    def wait_for_response(self):
        data = self.client.recv(2048).decode(FORMAT)
        return data

chat_client = ChatClient()

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