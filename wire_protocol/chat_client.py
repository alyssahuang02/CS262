import socket
import atexit
from commands import *
import time

class ChatClient:
    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)
    
    def disconnect(self):
        print("Network error detected. Disconecting and reconnecting...")
        self.send(purpose=LOGOUT,body=self.username)
        self.run()

    
    def run(self):
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
            self.show_users()
            self.receive_messages()

            # Try again because recipient invalid
            while self.send_chat_message() == False:
                pass
            self.receive_messages()

            self.delete_or_logout()
            self.receive_messages()
    

    def __init__(self, test=False):
        if test:
            return

        self.run()
    

    def show_users(self):
        found_user = False
        while not found_user:
            recipient = input("What users would you like to see? Enter nothing to skip.\n")

            if len(recipient) == 0:
                return

            if not self.send(purpose=SHOW_ACCOUNTS, body=recipient):
                print("Please enter a shorter regular expression.")
                continue

            response = self.receive()

            # Check if it's an error
            if response[PURPOSE] == NOTIFY and response[BODY] == USER_DOES_NOT_EXIST:
                continue
            
            # Otherwise, we have found the user
            found_user = True
        

    def enter_user(self, purpose):
        # Prompts user for username
        while True:
            username = input("What's your username?\n")
            if "/" in username:
                print("Username cannot contain '/'.")
                continue

            if len(username) != 0:
                break
        
        if purpose == "0":
            success = self.send(purpose=REGISTER,body=username)
            if not success:
                print("Please enter a shorter username.")
                return None, False
        elif purpose == "1":
            success = self.send(purpose=LOGIN,body=username)
            if not success:
                print("Please enter a shorter username.")
                return None, False
        
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
        self.username = username
        self.logged_in = logged_in
    

    def verify_recipient(self):
        while True:
            recipient = input("Who do you want to send a message to?\n")
            if len(recipient) != 0:
                    break
        success = self.send(purpose=CHECK_USER_EXISTS, body=recipient)
        if not success:
            print("Please enter a shorter username.")
            return None
        
        response = self.receive()

        if response[PURPOSE] == NOTIFY and response[BODY] == USER_DOES_NOT_EXIST:
            return None
        
        return recipient

    def verify_message(self, recipient):
        while True:
            message = input("What's your message?\n")
            if len(message) != 0:
                break

        success = self.send(purpose=SEND_MESSAGE, body=message, sender=self.username, recipient=recipient)
        if not success:
            print("Please enter a shorter message.")
            return False

        return True
        
    
    def send_chat_message(self):
        recipient = self.verify_recipient()
        while not recipient:
            recipient = self.verify_recipient()

        while not self.verify_message(recipient):
            pass
        
        response = self.receive()
    

    def receive_messages(self):
        if not self.logged_in:
            return
        
        self.send(purpose=PULL_MESSAGE, body=" ")

        response = self.receive()
        while True:
            if response[PURPOSE] == NO_MORE_DATA:
                return
            response = self.receive()
    

    def delete_or_logout(self):
        if not self.logged_in:
            return
        
        action = input("Enter 0 to delete your account. Enter 1 to logout. Enter anything else to continue.\n")
        
        if action == "0":
            self.send(purpose=DELETE_ACCOUNT, body=self.username)
            response = self.receive()
            if response[PURPOSE] == NOTIFY and response[BODY] == DELETION_SUCCESSFUL:
                self.logged_in = False
                self.username = None
                self.login()
        
        elif action == "1":
            self.send(purpose=LOGOUT,body=self.username)
            response = self.receive()
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


    def send(self, purpose, body, recipient=None, sender=None):
        msg = self.create_message(purpose, body, recipient, sender)
        try:
            encoded_message = msg.encode(FORMAT)
            if len(encoded_message) > MAX_BANDWIDTH:
                return False
            
            encoded_message = encoded_message.ljust(MAX_BANDWIDTH, b'0')
            self.client.send(encoded_message)
        except:
            raise ValueError
        
        return True

    
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
                parsed_message[part] = body[:length]
                break
            i += 1
        
        return parsed_message
    

    def receive(self):
        try:
            full_message = self.client.recv(MAX_BANDWIDTH).decode(FORMAT)
            parsed_message = self.parse_message(full_message)

            if parsed_message[PURPOSE] == NOTIFY and parsed_message[BODY] == DISCONNECT:
                self.disconnect()
                return

            if parsed_message[PURPOSE] == NOTIFY:
                body = parsed_message[BODY]
                print(body)

            return parsed_message
        
        except:
            return self.receive()

