import grpc
from commands import *
import grpc
import new_route_guide_pb2 as chat
import new_route_guide_pb2_grpc as grpc

class ChatClient:   
    def __init__(self):
        self.connection = None
        try:
            print(f"{SERVER}:{PORT}")
            self.connection = grpc.ChatStub(grpc.insecure_channel(f"{SERVER}:{PORT}"))
            print(self.connection)
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
            self.print_messages()
            # TODO: idk where to put this move later lol
            self.delete_account()

    def login(self):
        logged_in = False
        while not logged_in:
            action = input("Enter 0 to register. Enter 1 to login.\n")
            if action == "0":
                username, logged_in = self.enter_user(action)
            elif action == "1":
                username, logged_in = self.enter_user(action)
    
    def enter_user(self, purpose):
        # Prompts user for username
        username = input("What's your username?\n")

        new_text = chat.Text()
        new_text.text = username
        response = None
        if purpose == "0":
            response = self.connection.register_user(new_text)
        elif purpose == "1":
            response = self.connection.login_user(new_text)
        
        if response == LOGIN_SUCCESSFUL:
            self.logged_in = True
            self.username = username
            return username, True
        return username, False
    
    def send_chat_message(self):
        recipient = input("Who do you want to send a message to?\n")
        new_text = chat.Text()
        new_text.text = recipient
        response = self.connection.check_user_exists(new_text)

        if response == USER_DOES_NOT_EXIST:
            return
        
        message = input("What's your message?\n")
        new_message = chat.Note()
        new_message.sender = self.username
        new_message.recipient = recipient
        new_message.message = message

        output = self.connection.client_send_message(new_message)
        print(output)

    def print_messages(self):
        for message in self.receive_messages():
            print(message)

    def receive_messages(self):
        for note in self.connection.client_receive_message(chat.Empty()):
            yield f"[{note.sender} sent to {note.recipient}] {note.message}"

    def delete_account(self):
        action = input("Enter 0 to delete your account. Anything else to continue.\n")
        if action == "0":
            new_message = chat.Text()
            new_message.text = self.username

            response = self.connection.delete_account(new_message)
            if response == DELETION_SUCCESSFUL:
                self.logged_in = False
                self.username = None
                self.login()

chat_client = ChatClient()


    

