import pytest
from unittest.mock import patch, Mock
from new_client import ChatClient
from commands import *
from io import StringIO


# TODO: make sure tests run even when server is up


@pytest.fixture
def receiver_sender_message_to_server():
    return PURPOSE + SEPARATOR + SEND_MESSAGE + SEPARATOR + \
        RECIPIENT + SEPARATOR + "recipient" + SEPARATOR + \
        SENDER + SEPARATOR + "sender" + SEPARATOR + \
        LENGTH + SEPARATOR + str(len("message")) + SEPARATOR + \
        BODY + SEPARATOR + "message"


@pytest.fixture
def basic_message_to_server():
    return PURPOSE + SEPARATOR + LOGIN + SEPARATOR + \
        LENGTH + SEPARATOR + str(len("username")) + SEPARATOR + \
        BODY + SEPARATOR + "username"


@pytest.fixture
def receiver_sender_message_to_server():
    return PURPOSE + SEPARATOR + SEND_MESSAGE + SEPARATOR + \
        RECIPIENT + SEPARATOR + "recipient" + SEPARATOR + \
        SENDER + SEPARATOR + "sender" + SEPARATOR + \
        LENGTH + SEPARATOR + str(len("message")) + SEPARATOR + \
        BODY + SEPARATOR + "message"


@pytest.fixture
def notify_message_from_server():
    return PURPOSE + SEPARATOR + NOTIFY + SEPARATOR + \
        LENGTH + SEPARATOR + str(len(LOGIN_SUCCESSFUL)) + SEPARATOR + \
        BODY + SEPARATOR + LOGIN_SUCCESSFUL


@pytest.fixture
def no_more_data_message_from_server():
    return PURPOSE + SEPARATOR + NO_MORE_DATA + SEPARATOR + \
        LENGTH + SEPARATOR + str(len(" ")) + SEPARATOR + \
        BODY + SEPARATOR + " "


@pytest.fixture
def expected_stdout():
    return LOGIN_SUCCESSFUL + '\n'


@pytest.fixture
def parsed_message_notify():
    return {
        PURPOSE: NOTIFY,
        LENGTH: len(LOGIN_SUCCESSFUL),
        BODY: LOGIN_SUCCESSFUL
    }


@pytest.fixture
def parsed_message_no_more_data():
    return {
        PURPOSE: NO_MORE_DATA,
        LENGTH: len(" "),
        BODY: " "
    }

def test():
    client = ChatClient()
    msg = "!PURPOSE:/!NOTIFY/!LENGTH:/23/!BODY:/alyssa sends: hi dale 1!PURPOSE:/!NOTIFY/!LENGTH:/23/!BODY:/alyssa sends: hi dale 2!PURPOSE:/!NOTIFY/!LENGTH:/23/!BODY:/alyssa sends: hi dale 3!PURPOSE:/!NOMOREDATA/!LENGTH:/1/!BODY:/ "
    data = client.parse_messages(msg, [])
    assert data == ' '

# def test_create_message(basic_message_to_server, receiver_sender_message_to_server):
#     client = ChatClient()
#     data = client.create_message(LOGIN, "username")
#     assert data == basic_message_to_server

#     data = client.create_message(SEND_MESSAGE, "message", "recipient", "sender")
#     assert data == receiver_sender_message_to_server


# def test_parse_message(
#     notify_message_from_server, no_more_data_message_from_server, 
#     parsed_message_notify, parsed_message_no_more_data, expected_stdout
# ):
#     client = ChatClient()
#     with patch('sys.stdout', new = StringIO()) as mock_output:
#         data = client.parse_message(notify_message_from_server)
#         assert data == parsed_message_notify
#         assert mock_output.getvalue() == expected_stdout

#     with patch('sys.stdout', new = StringIO()) as mock_output:
#         data = client.parse_message(no_more_data_message_from_server)
#         assert data == parsed_message_no_more_data
#         assert mock_output.getvalue() == ''