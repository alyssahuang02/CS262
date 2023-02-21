import socket
import atexit
from commands import *

class ChatClient:
    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)
    
    def disconnect(self):
        print("Disconecting...")
        self.send(purpose=LOGOUT,body=self.username)
        self.client.close() # TODO: check this! idk if this is right
    

    def __init__(self, test=False):
        if not False:
            try:
                self.connect()
            except:
                print("Could not connect to server.")
                return
        
        atexit.register(self.disconnect)

        self.logged_in = False
        self.username = None

        while not self.logged_in:
            self.login()
        
        # Receive messages from when they were offline
        self.receive_messages()

        while self.logged_in:
            self.show_users()
            self.receive_messages()

            # Try again because user invalid
            while self.send_chat_message() == False:
                pass
            
            self.receive_messages()

            self.delete_or_logout()
            self.receive_messages()
    

    def show_users(self):
        found_user = False
        while not found_user:
            recipient = input("What users would you like to see? Enter nothing to skip.\n")

            if len(recipient) == 0:
                return

            self.send(purpose=SHOW_ACCOUNTS, body=recipient)
            response = self.receive()[0] # TODO: check this later

            # Check if it's an error
            if response[PURPOSE] == NOTIFY and response[BODY] == USER_DOES_NOT_EXIST:
                continue
            
            # Otherwise, we have found the user
            found_user = True
        

    def enter_user(self, purpose):
        # Prompts user for username
        username = input("What's your username?\n")
        if purpose == "0":
            self.send(purpose=REGISTER,body=username)
        elif purpose == "1":
            self.send(purpose=LOGIN,body=username)
        
        response = self.receive()[0] # TODO: bandaid solution
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
        self.username = username
        self.logged_in = logged_in
            
    
    def send_chat_message(self):
        recipient = input("Who do you want to send a message to?\n")
        self.send(purpose=CHECK_USER_EXISTS, body=recipient)
        response = self.receive()[0] # TODO: bandaid solution

        if response[PURPOSE] == NOTIFY and response[BODY] == USER_DOES_NOT_EXIST:
            return False
        
        message = input("What's your message?\n")
        self.send(purpose=SEND_MESSAGE, body=message, sender=self.username, recipient=recipient)
        response = self.receive()[0] # TODO: bandaid solution
        return True
    

    def receive_messages(self):
        if not self.logged_in:
            return
        
        self.send(purpose=PULL_MESSAGE, body="")

        no_more_data = False
        responses = self.receive()
        while no_more_data == False:
            for response in responses:
                if response[PURPOSE] == NO_MORE_DATA:
                    no_more_data = True
                    print("No more messages.")
                    return
            responses = self.receive()
    

    def delete_or_logout(self):
        if not self.logged_in:
            return
        
        action = input("Enter 0 to delete your account. Enter 1 to logout. Enter anything else to continue.\n")
        
        if action == "0":
            self.send(purpose=DELETE_ACCOUNT, body=self.username)
            response = self.receive()[0] # TODO: bandaid solution
            if response[PURPOSE] == NOTIFY and response[BODY] == DELETION_SUCCESSFUL:
                self.logged_in = False
                self.username = None
                self.login()
        
        elif action == "1":
            self.send(purpose=LOGOUT,body=self.username)
            response = self.receive()[0] # TODO: bandaid solution
            if response[PURPOSE] == NOTIFY and response[BODY] == LOGOUT_SUCCESSFUL:
                self.logged_in = False
                self.username = None
                self.login()

    
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

    
    # Can be multiple messages in one full_message
    def parse_messages(self, full_message, parsed_messages):
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

                # considering the case where there are multiple messages
                if len(body) > length:
                    remainder_of_message = body[length:]
                    end_parsed = self.parse_messages(remainder_of_message, [])
                    parsed_messages += end_parsed
                
                return [parsed_message] + parsed_messages
            i += 1
        
        # TODO/CHECK: can we have it such that a message is too long to be sent in one go
        # WHAT DO WE DO THEN
        return parsed_messages
    

    def receive(self):
        try:
            full_message = self.client.recv(MAX_BANDWIDTH).decode(FORMAT)
        except:
            raise ValueError
        
        parsed_messages = self.parse_messages(full_message, [])

        for parsed_message in parsed_messages:
            if parsed_message[PURPOSE] == NOTIFY:
                body = parsed_message[BODY]
                print(body)

        return parsed_messages
