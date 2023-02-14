import socket
import pickle # we can't use this in our final implementation according to waldo

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "10.250.10.42" # TODO: need to change later/have some way to make it dynamic
ADDR = (SERVER, PORT)
LOGIN_SUCCESS = "!LOGGEDIN"
NO_MORE_DATA = "!NOMOREDATA"
PULL_MESSAGE = "!PULL"
SEND_MESSAGE = "!SEND"
LOGIN = "!LOGIN"
REGISTER = "!REGISTER"
PURPOSE = "!PURPOSE:"
RECIPIENT = "!RECIPIENT:"
SENDER = "!SENDER:"
LENGTH = "!LENGTH:"
BODY = "!BODY:"
SEPARATOR = "/"

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

    def enter_user(self, purpose):
        # Prompts user for username
        username = input("What's your username?")
        if purpose == "0":
            msg = self.create_message(purpose=REGISTER, body=username)
        elif purpose == "1":
            msg = self.create_message(purpose=LOGIN, body=username)
        self.send(msg)
        response = self.receive()
        if response == LOGIN_SUCCESS:
            self.logged_in = True
            self.username = username
            return username, True
        else:
            return username, False

    def login(self):
        logged_in = False
        while not logged_in:
            action = input("Enter 0 to register. Enter 1 to login.")
            if action == "0":
                username, logged_in = self.enter_user(action)
            elif action == "1":
                username, logged_in = self.enter_user(action)
            else:
                self.send("Invalid input.")

    def send_chat_message(self):
        self.send(SEND_MESSAGE)
        # TODO: literally zero error handling
        self.send(self.username)

        prompt = self.receive()
        print(prompt)

        recipient = input()
        self.send(recipient)

        prompt = self.receive()
        print(prompt)

        message = input()
        self.send(message)

        print("Message sent!")
    
    def create_message(self, purpose, body, recipient=None, sender=None):
        data=PURPOSE + purpose
        if recipient and sender:
            data += SEPARATOR + RECIPIENT + recipient
            data += SEPARATOR + SENDER + sender
        if body:
            length = len(body)
            data+= SEPARATOR + LENGTH + length
            data+= SEPARATOR + BODY + body
        return data

    def decode_message(self, msg):
        return


    def receive_messages(self):
        msg = self.create_message(PULL_MESSAGE, "")
        self.send(msg)
        response = self.receive()
        while response != NO_MORE_DATA:
            print(response)
            response = self.receive()
        
        print("No more messages.")


    def disconnect(self):
        pass


    def send(self, msg):
        # message = msg.encode(FORMAT)
        # msg_length = len(message)
        # send_length = str(msg_length).encode(FORMAT)
        # send_length += b' ' * (HEADER - len(send_length))
        # self.client.send(send_length)
        try:
            self.client.send(msg.encode(FORMAT))
        except:
            raise ValueError

    
    def receive(self):
        try:
            return self.client.recv(HEADER).decode(FORMAT)
        except:
            raise ValueError

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