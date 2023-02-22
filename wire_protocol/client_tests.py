from chat_client import ChatClient
from commands import *
from test_fixtures import *

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
    data = client.create_message(PULL_MESSAGE, " ")
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
    message = client.parse_message(notify_message_login_successful)

    assert message[PURPOSE] == NOTIFY
    assert message[LENGTH] == '17'
    assert message[BODY] == "Login successful!"


def test_receive_messages(receive_single_message, receive_no_more_data):
    client = ChatClient(test=True)

    # Testing receiving a single message
    message = client.parse_message(receive_single_message)
    assert message[PURPOSE] == NOTIFY
    assert message[LENGTH] == '21'
    assert message[BODY] == "alyssa sends: hi dale"

    # No more data after
    no_more_data = client.parse_message(receive_no_more_data)
    assert no_more_data[PURPOSE] == NO_MORE_DATA
    assert no_more_data[LENGTH] == '1'
    assert no_more_data[BODY] == " "
