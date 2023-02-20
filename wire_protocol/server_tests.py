from chat_server import ChatServer
from commands import *
from test_fixtures import *


# TODO: make sure tests run even when server is up

# pytest client_tests.py

# TODO: i havent run this just temp setup lolz

def test_register(register_message):
    # Testing parsing a register message
    server = ChatServer()
    data = server.parse_message(register_message)
    assert len(data) == 1
    message = data[0]
    assert message[PURPOSE] == REGISTER
    assert message[LENGTH] == 4
    assert message[BODY] == "dale"