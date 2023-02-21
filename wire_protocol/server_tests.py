from chat_server import ChatServer
from commands import *
from test_fixtures import *


# TODO: make sure tests run even when server is up

# pytest server_tests.py

def test_register(register_message):
    # Testing parsing a register message
    server = ChatServer(test=True)

    message = server.parse_message(register_message)
    assert message[PURPOSE] == REGISTER
    assert message[LENGTH] == '4'
    assert message[BODY] == "dale"


def test_login(login_message):
    # Testing parsing a login message
    server = ChatServer(test=True)

    message = server.parse_message(login_message)
    assert message[PURPOSE] == LOGIN
    assert message[LENGTH] == '4'
    assert message[BODY] == "dale"


def test_show_accounts(show_accounts_message):
    # Testing parsing a show accounts message
    server = ChatServer(test=True)

    message = server.parse_message(show_accounts_message)
    assert message[PURPOSE] == SHOW_ACCOUNTS
    assert message[LENGTH] == '4'
    assert message[BODY] == "dale"


def test_check_user_exists_message(check_user_exists_message):
    # Testing parsing a checking user exists message
    server = ChatServer(test=True)

    message = server.parse_message(check_user_exists_message)
    assert message[PURPOSE] == CHECK_USER_EXISTS
    assert message[LENGTH] == '4'
    assert message[BODY] == "dale"


def test_pull(pull_message):
    # Testing parsing a pull message
    server = ChatServer(test=True)

    message = server.parse_message(pull_message)
    assert message[PURPOSE] == PULL_MESSAGE


def test_delete_account(delete_account_message):
    # Testing parsing a delete account message
    server = ChatServer(test=True)

    message = server.parse_message(delete_account_message)
    assert message[PURPOSE] == DELETE_ACCOUNT
    assert message[LENGTH] == '4'
    assert message[BODY] == "dale"


def test_logout(logout_message):
    # Testing parsing a logout message
    server = ChatServer(test=True)

    message = server.parse_message(logout_message)
    assert message[PURPOSE] == LOGOUT
    assert message[LENGTH] == '4'
    assert message[BODY] == "dale"


def test_send_notify(notify_message_login_successful):
    # Testing sending a notify message
    server = ChatServer(test=True)
    data = server.create_message(NOTIFY, "Login successful!")
    assert data == notify_message_login_successful


def test_send_message(send_single_message):
    # Testing sending a chat message
    server = ChatServer(test=True)
    data = server.create_message(NOTIFY, "alyssa sends: hi dale")
    assert data == send_single_message[0]

    data = server.create_message(NO_MORE_DATA, " ")
    assert data == send_single_message[1]
