import pytest
from unittest.mock import patch, Mock
from new_client import ChatClient
from commands import *

@pytest.fixture
def receiver_sender_message():
    return SEND_MESSAGE + SEPARATOR + "message" + SEPARATOR + "recipient" + SEPARATOR + "sender"


@pytest.fixture
def basic_message():
    return LOGIN + SEPARATOR + "username"


def test_create_message(basic_message, receiver_sender_message):
    client = ChatClient()
    data = client.create_message(LOGIN, "username")
    assert data == basic_message

    data = client.create_message(SEND_MESSAGE, "message", "recipient", "sender")
    assert data == receiver_sender_message


# @patch(
#     'new_client.ChatClient',
#     Mock(return_value=None)
# )
# def test():
#     assert True

# @pytest.fixture
# def example_fixture():
#     return 1

# def test_with_fixture(example_fixture):
#     assert example_fixture == 1