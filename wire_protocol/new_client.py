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
NOTIFY = "!NOTIFY"

MAX_BANDWIDTH = 2048 # TODO: WE HAVE TO CHECK STUFF DOES NOT EXCEED THIS

CHECK_USER_EXISTS = "!CHECKUSEREXISTS"
DELETE_ACCOUNT = "!DELETEACCOUNT"

# Printable messages from NOTIFY
LOGIN_SUCCESSFUL = "Login successful!"
USER_DOES_NOT_EXIST = "User does not exist."
DELETION_SUCCESSFUL = "Account deleted."
LOGOUT_SUCCESSFUL = "Logout successful."

class ChatClient:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)

        self.logged_in = False
        self.username = None

        while not self.logged_in:
            self.login()
        
        # Receive messages from when they were offline
        self.receive_messages()
        
        while self.logged_in:
            # TODO: check ordering
            self.send_chat_message()
            self.receive_messages()
            # TODO: idk where to put this move later lol
            self.delete_account()

    def enter_user(self, purpose):
        # Prompts user for username
        username = input("What's your username?\n")
        if purpose == "0":
            self.send(purpose=REGISTER,body=username)
            # msg = self.create_message(purpose=REGISTER, body=username)
        elif purpose == "1":
            self.send(purpose=LOGIN,body=username)
            # msg = self.create_message(purpose=LOGIN, body=username)
        
        response = self.receive()
        if response[PURPOSE] == NOTIFY and response[BODY] == LOGIN_SUCCESSFUL:
            self.logged_in = True
            self.username = username
            return username, True
        
        return username, False

    def login(self):
        logged_in = False
        while not logged_in:
            action = input("Enter 0 to register. Enter 1 to login.\n")
            if action == "0":
                username, logged_in = self.enter_user(action)
            elif action == "1":
                username, logged_in = self.enter_user(action)
            
    
    def send_chat_message(self):
        recipient = input("Who do you want to send a message to?\n")
        self.send(purpose=CHECK_USER_EXISTS, body=recipient)
        response = self.receive()

        if response[PURPOSE] == NOTIFY and response[BODY] == USER_DOES_NOT_EXIST:
            return
        
        message = input("What's your message?\n")
        self.send(purpose=SEND_MESSAGE, body=message, sender=self.username, recipient=recipient)
        print(self.receive())
    
    def receive_messages(self):
        self.send(purpose=PULL_MESSAGE, body="")
        response = self.receive()
        while response[PURPOSE] != NO_MORE_DATA:
            response = self.receive()
        
        print("No more messages.")
    

    def delete_account(self):
        action = input("Enter 0 to delete your account.\n")
        if action == "0":
            self.send(purpose=DELETE_ACCOUNT, body=self.username)
            response = self.receive()
            if response[PURPOSE] == NOTIFY and response[BODY] == DELETION_SUCCESSFUL:
                self.logged_in = False
                self.username = None
                self.login()


    def disconnect(self):
        pass

    
    def create_message(self, purpose, body, recipient=None, sender=None):
        data=PURPOSE + SEPARATOR + purpose
        if recipient and sender:
            data += SEPARATOR + RECIPIENT + SEPARATOR + recipient
            data += SEPARATOR + SENDER + SEPARATOR + sender
        if body:
            length = len(body)
            data += SEPARATOR + LENGTH + SEPARATOR + str(length)
            data += SEPARATOR + BODY + SEPARATOR + body
        
        return data


    def send(self,purpose, body, recipient=None, sender=None):
        msg = self.create_message(purpose, body, recipient, sender)
        try:
            self.client.send(msg.encode(FORMAT))
        except:
            raise ValueError

    
    def receive(self):
        try:
            full_message = self.client.recv(MAX_BANDWIDTH).decode(FORMAT)
        except:
            raise ValueError
        split_message = full_message.split("/")
        parsed_message = {}
        i = 0
        while i < len(split_message):
            part = split_message[i]
            if BODY != part:
                parsed_message[part] = split_message[i+1]
                i += 1
            else:
                body = "/".join(split_message[i+1:])
                length = int(parsed_message[LENGTH])
                parsed_message[part] = body[:length]
                break
            i += 1
        
        if parsed_message[PURPOSE] == NOTIFY:
            body = parsed_message[BODY]
            print(body)
        return parsed_message
        



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