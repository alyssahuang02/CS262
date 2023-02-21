from chat_client import ChatClient
from commands import *
from test_fixtures import *


# TODO: make sure tests run even when server is up

# pytest client_tests.py

def test_register(register_message):
    # Testing sending a register message
    client = ChatClient(test=True)
    data = client.create_message(REGISTER, "dale")
    assert data == register_message


def test_login(login_message):
    # Testing sending a login message
    client = ChatClient(test=True)
    data = client.create_message(LOGIN, "dale")
    assert data == login_message


def test_show_accounts(show_accounts_message):
    # Testing sending a login message
    client = ChatClient(test=True)
    data = client.create_message(SHOW_ACCOUNTS, "dale")
    assert data == show_accounts_message


def test_check_user_exists_message(check_user_exists_message):
    # Testing sending a login message
    client = ChatClient(test=True)
    data = client.create_message(CHECK_USER_EXISTS, "dale")
    assert data == check_user_exists_message


def test_pull(pull_message):
    # Testing sending a login message
    client = ChatClient(test=True)
    data = client.create_message(PULL_MESSAGE, "")
    assert data == pull_message


def test_delete_account(delete_account_message):
    # Testing sending a login message
    client = ChatClient(test=True)
    data = client.create_message(DELETE_ACCOUNT, "dale")
    assert data == delete_account_message


def test_logout(logout_message):
    # Testing sending a login message
    client = ChatClient(test=True)
    data = client.create_message(LOGOUT, "dale")
    assert data == logout_message


def test_parse_notify(notify_message_login_successful):
    # Testing parsing a notify message
    client = ChatClient(test=True)
    data = client.parse_messages(notify_message_login_successful, [])

    assert len(data) == 1
    message = data[0]
    assert message[PURPOSE] == NOTIFY
    assert message[LENGTH] == 17
    assert message[BODY] == "Login successful!"


def test_receive_messages(receive_single_message, receive_multiple_messages):
    client = ChatClient(test=True)

    # Testing receiving a single message
    data = client.parse_messages(receive_single_message, [])

    assert len(data) == 2
    message = data[0]
    assert message[PURPOSE] == NOTIFY
    assert message[LENGTH] == 21
    assert message[BODY] == "alyssa sends: hi dale"

    # No more data after
    no_more_data = data[1]
    assert no_more_data[PURPOSE] == NO_MORE_DATA
    assert no_more_data[LENGTH] == 1
    assert no_more_data[BODY] == " "

    # Testing receiving multiple messages
    data = client.parse_messages(receive_multiple_messages, [])

    assert len(data) == 4
    message = data[0]
    assert message[PURPOSE] == NOTIFY
    assert message[LENGTH] == 23
    assert message[BODY] == "alyssa sends: hi dale 1"

    message = data[1]
    assert message[PURPOSE] == NOTIFY
    assert message[LENGTH] == 23
    assert message[BODY] == "alyssa sends: hi dale 2"

    message = data[2]
    assert message[PURPOSE] == NOTIFY
    assert message[LENGTH] == 23
    assert message[BODY] == "alyssa sends: hi dale 3"

    # No more data after
    no_more_data = data[3]
    assert no_more_data[PURPOSE] == NO_MORE_DATA
    assert no_more_data[LENGTH] == 1
    assert no_more_data[BODY] == " "