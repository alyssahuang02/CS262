import grpc
from grpc._server import _Server
import new_route_guide_pb2
import new_route_guide_pb2_grpc

import socket 
import threading
from concurrent import futures
import re
from commands import *

import threading

mutex_unsent_messages = threading.Lock()
mutex_accounts = threading.Lock()
mutex_active_accounts = threading.Lock()

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
        username = request.text
        
        if username not in self.accounts:
            return new_route_guide_pb2.Text(text="Username does not exist.")
        else:
            # Log in user
            mutex_active_accounts.acquire()
            self.active_accounts[username] = context.peer()
            mutex_active_accounts.release()
        
        return new_route_guide_pb2.Text(text=LOGIN_SUCCESSFUL)

    def register_user(self, request, context):
        username = request.text
        if username in self.accounts:
            return new_route_guide_pb2.Text(text="Username already exists.")
        else:
            print(f"Registering {username}")
            # Register and log in user
            mutex_active_accounts.acquire()
            self.active_accounts[username] = context.peer()
            mutex_active_accounts.release()

            mutex_accounts.acquire()
            self.accounts.append(username)
            mutex_accounts.release()

            mutex_unsent_messages.acquire()
            self.unsent_messages[username] = []
            mutex_unsent_messages.release()
            return new_route_guide_pb2.Text(text=LOGIN_SUCCESSFUL)
        
    def check_user_exists(self, request, context):
        username = request.text
        if username in self.accounts:
            return new_route_guide_pb2.Text(text="User exists.")
        else:
            return new_route_guide_pb2.Text(text=USER_DOES_NOT_EXIST)
        
    def client_receive_message(self, request, context):
        lastindex = 0
        recipient = request.text
        while len(self.unsent_messages[recipient]) > lastindex:
            sender, message = self.unsent_messages[recipient][lastindex]
            lastindex += 1
            formatted_message = new_route_guide_pb2.Note()
            formatted_message.recipient = recipient
            formatted_message.sender = sender
            formatted_message.message = message
            yield formatted_message

    def client_send_message(self, request, context):
        # self.unsent_messages.append(request)
        recipient = request.recipient
        sender = request.sender
        message = request.message
        mutex_unsent_messages.acquire()
        self.unsent_messages[recipient].append((sender, message))
        mutex_unsent_messages.release()
        return new_route_guide_pb2.Text(text="Message sent!")

    def delete_account(self, request, context):
        username = request.text
        try: 
            mutex_active_accounts.acquire()
            del self.active_accounts[username]
            mutex_active_accounts.release()

            mutex_unsent_messages.acquire()
            del self.unsent_messages[username]
            mutex_unsent_messages.release()

            mutex_accounts.acquire()
            self.accounts.remove(username)
            mutex_accounts.release()
        except:
            return new_route_guide_pb2.Text(text=DELETION_UNSUCCESSFUL)
        return new_route_guide_pb2.Text(text=DELETION_SUCCESSFUL)
    
    def display_accounts(self, request, context):
        none_found = True
        username = request.text
        for account in self.accounts:
            x = re.search(username, account)
            if x is not None:
                none_found = False
                yield new_route_guide_pb2.Text(text = x.string)
        if none_found:
            yield new_route_guide_pb2.Text(text = "No user matches this!")

    # Precondition: we have already checked that the username corresponds to
    # the user who was logged in at the time
    def logout(self, request, context):
        username = request.text
        mutex_active_accounts.acquire().acquire()
        del self.active_accounts[username]
        mutex_active_accounts.acquire().release()

        return new_route_guide_pb2.Text(text=LOGOUT_SUCCESSFUL)

class ServerRunner:
    """Class for running server backend functionality."""

    def __init__(self, ip = "localhost"):
        """Initialize a server instance."""
        # self.ip = socket.gethostbyname(socket.gethostname()) if ip is None else ip
        self.ip = SERVER
        self.port = PORT

        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        self.chat_servicer = ChatServicer()

    def start(self):
        """Function for starting server."""
        new_route_guide_pb2_grpc.add_ChatServicer_to_server(self.chat_servicer, self.server)
        self.server.add_insecure_port(f"[::]:{self.port}")
        self.server.start()
        self.server.wait_for_termination()

    def stop(self):
        """Function for stopping server."""
        self.server.stop(grace=None)
        self.thread_pool.shutdown(wait=False)


chat_server = ServerRunner()
print("[STARTING] server is starting...")
chat_server.start()