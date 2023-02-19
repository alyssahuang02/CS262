from grpc import server
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
        print(context.peer())

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
        print("context!!", context)
        lastindex = 0
        while True:
            while len(self.unsent_messages) > lastindex:
                new_message = self.unsent_messages[lastindex]
                lastindex += 1
                yield new_message

    def client_send_message(self, request, context):
        self.unsent_messages.append(request)
        return new_route_guide_pb2.Text(text="Message sent!")

    def delete_account(self, request, context):
        username = request.text
        mutex_active_accounts.acquire()
        del self.active_accounts[username]
        mutex_active_accounts.release()

        mutex_unsent_messages.acquire()
        del self.unsent_messages[username]
        mutex_unsent_messages.release()

        mutex_accounts.acquire()
        self.accounts.remove(username)
        mutex_accounts.release()

        return new_route_guide_pb2_grpc.Text(text=DELETION_SUCCESSFUL)

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
        self.ip = socket.gethostbyname(socket.gethostname()) if ip is None else ip
        self.port = PORT

        self.server = server(futures.ThreadPoolExecutor(max_workers=10))
        self.chat_servicer = ChatServicer()

    def start(self):
        """Function for starting server."""
        new_route_guide_pb2_grpc.add_ChatServicer_to_server(self.chat_servicer, self.server)
        print("ip and port", self.ip, self.port)
        # self.server.add_insecure_port("[::]:5050")
        self.server.add_insecure_port(f"{self.ip}:{self.port}")
        self.server.start()
        self.server.wait_for_termination()

    def stop(self):
        """Function for stopping server."""
        self.server.stop(grace=None)
        self.thread_pool.shutdown(wait=False)


chat_server = ServerRunner()
print("[STARTING] server is starting...")
chat_server.start()