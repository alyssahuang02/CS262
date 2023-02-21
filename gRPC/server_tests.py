from server import ChatServicer
from commands import *
from unittest.mock import MagicMock
from unittest.mock import patch
import new_route_guide_pb2
from io import StringIO

# pytest server_tests.py

def test_login_flow():
    # Testing login flow
    server = ChatServicer()

    # Setting up mocks
    new_route_guide_pb2.Text=MagicMock()
    request = MagicMock()
    request.text = "dale"
    context = MagicMock()
    context.peer = MagicMock(return_value="mock ip address")

    # Test username does not exist
    assert len(server.accounts) == 0
    server.login_user(request, context)
    new_route_guide_pb2.Text.assert_called_with(text="Username does not exist.")

    # Test user already logged in
    server.accounts.append("dale")
    server.active_accounts["dale"] = "mock ip address"

    server.login_user(request, context)
    new_route_guide_pb2.Text.assert_called_with(text="User is already logged in.")

    # Test successful login
    server.active_accounts = {}
    assert len(server.accounts) == 1

    server.login_user(request, context)
    context.peer.assert_called_once()
    new_route_guide_pb2.Text.assert_called_with(text=LOGIN_SUCCESSFUL)
