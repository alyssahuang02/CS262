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
            self.send(purpose=REGISTER,body=username)
            # msg = self.create_message(purpose=REGISTER, body=username)
        elif purpose == "1":
            self.send(purpose=LOGIN,body=username)
            # msg = self.create_message(purpose=LOGIN, body=username)
        
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
            
    def send_chat_message(self):
        recipient = input("Who do you want to send a message to?")
        message = input("What's your message?")
        self.send(purpose=SEND_MESSAGE, body=message, sender=self.username, recipient=recipient)
        print(self.receive())
    
    def receive_messages(self):
        self.send(purpose=PULL_MESSAGE, body="")
        response = self.receive()
        while response[BODY] != NO_MORE_DATA:
            print(response[BODY])
            response = self.receive()
        
        print("No more messages.")


    def disconnect(self):
        pass


    def send(self,purpose, body, recipient=None, sender=None):
        data=PURPOSE + purpose
        if recipient and sender:
            data += SEPARATOR + RECIPIENT + recipient
            data += SEPARATOR + SENDER + sender
        if body:
            length = len(body)
            data+= SEPARATOR + LENGTH + length
            data+= SEPARATOR + BODY + body
    
        try:
            self.client.send(data.encode(FORMAT))
        except:
            raise ValueError

    
    def receive(self):
        try:
            full_message = self.client.recv(HEADER).decode(FORMAT)
            split_message = full_message.split("/")
            parsed_message = {}
            for i in range(len(split_message)):
                part = split_message[i]
                if part != BODY:
                    parsed_message[part] = split_message[i+1]
                    i += 1
                else:
                    body = split_message[i+1:].join("/")
                    length = int(parsed_message[LENGTH])
                    parsed_message[part] = body[:length]
                    break
            return parsed_message
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