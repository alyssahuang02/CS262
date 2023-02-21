from client import ChatClient
from commands import *
from unittest.mock import MagicMock
from unittest.mock import patch
from io import StringIO


def test_registration_flow():
    # Testing registration flow
    client = ChatClient(test=True)

    # Setting up mocks
    client.logged_in = False
    client.username = None
    client.connection = MagicMock()
    client.connection.register_user = MagicMock(return_value=MagicMock(text=LOGIN_SUCCESSFUL))

    # Test registration
    with patch("builtins.input", side_effect=["0", "dale"]):
        assert not client.logged_in
        assert not client.username

        client.login()

        client.connection.register_user.assert_called_once()
        assert client.logged_in
        assert client.username == "dale"


def test_login_flow():
    # Testing login flow
    client = ChatClient(test=True)

    # Setting up mocks
    client.logged_in = False
    client.username = None
    client.connection = MagicMock()
    client.connection.login_user = MagicMock(return_value=MagicMock(text=LOGIN_SUCCESSFUL))

    # Test registration
    with patch("builtins.input", side_effect=["1", "dale"]):
        assert not client.logged_in
        assert not client.username

        client.login()

        client.connection.login_user.assert_called_once()
        assert client.logged_in
        assert client.username == "dale"


def test_display_accounts():
    # Testing display accounts
    client = ChatClient(test=True)

    # Setting up mocks
    client.connection = MagicMock()
    client.connection.display_accounts = MagicMock(return_value=[MagicMock(text="dale"), MagicMock(text="dallen")])

    # Test registration
    with patch("builtins.input", side_effect=["dale"]):
        with patch('sys.stdout', new = StringIO()) as terminal_output:
            client.display_accounts()
            client.connection.display_accounts.assert_called_once()

            assert terminal_output.getvalue() == "\nUsers:\ndale\ndallen\n"


# TODO: send chat message, delete and logout