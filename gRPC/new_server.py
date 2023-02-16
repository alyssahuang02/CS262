import grpc
import new_route_guide_pb2
import new_route_guide_pb2_grpc

import socket 
import threading
import re
from commands import *

import threading

mutex = threading.Lock()

class ChatServicer(new_route_guide_pb2_grpc.ChatServicer):
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDR)

        # TODO: will need to use a mutex lock for each of these likely
        self.unsent_messages = {} # {username: [msg1, msg2, msg3]}
        self.accounts = [] # [username1, username2, username3]
        self.active_accounts = {} # {username: addr}

    def login_user(self, request, context):
        logged_in = False
        print(context.peer())
        
        if request not in self.accounts:
            return new_route_guide_pb2.Text(text="Username does not exist.")
        else:
            # Log in user
            mutex.acquire()
            self.active_accounts[request] = context.peer()
            mutex.release()
            logged_in = True
        
        return new_route_guide_pb2.Text(text=LOGIN_SUCCESSFUL)

    def register_user(self, request, context):
        if request in self.accounts:
            return new_route_guide_pb2.Text(text="Username already exists.")
        else:
            # Register and log in user
            mutex.acquire()
            self.active_accounts[request] = context.peer()
            self.accounts.append(request)
            self.unsent_messages[request] = []
            mutex.release()
            registered = True
            return new_route_guide_pb2.Text(text=LOGIN_SUCCESSFUL)

    def record_chat_message(self, request, context):
        mutex.acquire()
        self.unsent_messages[request.recipient].append((request.sender, request.message))
        mutex.release()
        return new_route_guide_pb2.Text(text="Message sent!")
    
    def send_unsent_messages(self, request, context):
        # mutex.acquire()
        for recipient in self.unsent_messages:
            messages = self.unsent_messages[request.recipient]

            if recipient in self.active_accounts:
                recipient_addr = self.active_accounts[request.recipient]
                if recipient_addr == context.peer():
                    for message in messages:
                        text = message[0] + " sends: " + message[1]
                        return new_route_guide_pb2.Text(text=text)
                    
            # TODO: do this in a thread-safe way lmao
            # TODO: Need to modify this to delete stuff
            # WHAT IF THE RECIPIENT DISCONNECTS?
            self.unsent_messages[request.recipient] = []
        # mutex.release()
        return new_route_guide_pb2.Text(text=NO_MORE_DATA)

    def delete_account(self, request, context):
        mutex.acquire()
        del self.active_accounts[request.text]
        del self.unsent_messages[request.text]
        self.accounts.remove(request.text)
        mutex.release()
        return new_route_guide_pb2.Text(text=DELETION_SUCCESSFUL)
    

    # Precondition: we have already checked that the username corresponds to
    # the user who was logged in at the time
    def logout(self, request, context):
        mutex.acquire()
        del self.active_accounts[request.text]
        mutex.release()
        return new_route_guide_pb2.Text(text=LOGOUT_SUCCESSFUL)

    def handle_client(self, parsed_message, context):
        print(f"[NEW CONNECTION] {context.peer()} connected.")
        logged_in = False

        # while not disconnected
        while True:
            print(parsed_message)
            purpose = parsed_message.text[PURPOSE]
            if purpose == LOGIN:
                username = parsed_message.text[BODY]
                username, logged_in = self.login_user(username, context)
            elif purpose == REGISTER:
                username = parsed_message[BODY]
                username, logged_in = self.register_user(username, context)
            elif purpose == SEND_MESSAGE:
                if not logged_in:
                    return new_route_guide_pb2.Text(text="You must be logged in to send a message.")
                sender = parsed_message[SENDER]
                recipient = parsed_message[RECIPIENT]
                msg = parsed_message[BODY]
                self.record_chat_message(sender, recipient, msg)
            elif purpose == PULL_MESSAGE:
                if not logged_in:
                    self.send(conn, NOTIFY, "You must be logged in to receive messages.")
                    continue

                self.send_unsent_messages(conn, addr)
            elif purpose == CHECK_USER_EXISTS:
                username = parsed_message[BODY]
                if username in self.accounts:
                    self.send(conn, NOTIFY, "User exists.")
                else:
                    self.send(conn, NOTIFY, USER_DOES_NOT_EXIST)
            
            elif purpose == DELETE_ACCOUNT:
                if not logged_in:
                    self.send(conn, NOTIFY, "You must be logged in to delete an account.")
                    continue
                username = parsed_message[BODY]

                # Checks that the user currently logged in is the one who is trying to delete their account
                for user in self.active_accounts:
                    if user == username and self.active_accounts[user] == addr:
                        self.delete_account(conn, username)
                        continue
                self.send(conn, NOTIFY, "You cannot another user's account.")
                continue
            
            elif purpose == SHOW_ACCOUNTS:
                username = parsed_message[BODY]
                matched_accounts = []
            
                mutex.acquire()
                for account in self.accounts:
                    x = re.search(username, account)
                    if x is not None:
                        matched_accounts.append(account)
                mutex.release()
                if len(matched_accounts) == 0:
                    self.send(conn, NOTIFY, USER_DOES_NOT_EXIST)
                else:
                    # might throw an error with lists
                    self.send(conn, NOTIFY, matched_accounts)

