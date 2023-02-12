import socket
import pickle # we can't use this in our final implementation according to waldo

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "dhcp-10-250-18-31.harvard.edu" # TODO: need to change later/have some way to make it dynamic
ADDR = (SERVER, PORT)
LOGIN_SUCCESS = "!LOGGEDIN"
NO_MORE_DATA = "!NOMOREDATA"

class ChatClient:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)

        self.logged_in = False
        self.username = None

        while not self.logged_in:
            self.login()
        
        print("Logged in!")
        
        # Receive messages from when they were offline
        self.receive_messages()
        
        while self.logged_in:
            # TODO: check ordering
            self.send_chat_message()
            self.receive_messages()

    
    def login(self):
        # Prints prompt from server
        prompt = self.wait_for_response()
        print(prompt)

        # Sends user action to server
        action = input()
        self.send(action)

        # Username prompt or "invalid input" message
        action_response = self.wait_for_response()
        print(action_response)
        if action_response == "Invalid input.":
            return

        # Gets username from user and sends it to server
        username = input()
        self.send(username)

        # Gets response from server (either success or error message)
        response = self.wait_for_response()

        # Checks if the login was successful and stores information if so
        if response == LOGIN_SUCCESS:
            self.logged_in = True
            self.username = username
        else:
            print(response)


    def send_chat_message(self):
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
    

    def receive_messages(self):
        response = self.wait_for_response()
        while response != NO_MORE_DATA:
            print(response)
            response = self.wait_for_response()
        
        print("No more messages.")

    def disconnect(self):
        pass


    def send(self, msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)

    
    def wait_for_response(self):
        msg_length = self.client.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            response = self.client.recv(msg_length).decode(FORMAT)
            return response
        self.wait_for_response()

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