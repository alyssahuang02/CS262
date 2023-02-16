import socket
from commands import *

class ChatClient:
    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)
    
    def __init__(self):
        try:
            self.connect()
        except:
            print("Could not connect to server.")
            return

        self.logged_in = False
        self.username = None

        while not self.logged_in:
            self.login()
        
        # Receive messages from when they were offline
        self.receive_messages()
        
        while self.logged_in:
            # TODO: check ordering
            # self.show_users()
            self.send_chat_message()
            self.receive_messages()
            # TODO: idk where to put this move later lol
            self.delete_account()
    
    def show_users(self):
        found_user = False
        while not found_user:
            recipient = input("What users would you like to see?\n")
            self.send(purpose=SHOW_ACCOUNTS, body=recipient)
            response = self.receive()

            if response[PURPOSE] == NOTIFY and response[BODY] == USER_DOES_NOT_EXIST:
                print("No user matches that pattern. Try again.")
            else:
                print(response[BODY])
                found_user = True
        

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
        response = self.receive()
    

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

    
    def parse_message(self, full_message):
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
                parsed_message[LENGTH] = length
                parsed_message[part] = body[:length]
                break
            i += 1

        if parsed_message[PURPOSE] == NOTIFY:
            body = parsed_message[BODY]
            print(body)
        return parsed_message
    

    def receive(self):
        try:
            full_message = self.client.recv(MAX_BANDWIDTH).decode(FORMAT)
        except:
            raise ValueError
        return self.parse_message(full_message)
        

chat_client = ChatClient()
