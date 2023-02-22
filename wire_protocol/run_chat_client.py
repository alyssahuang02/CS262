from chat_client import ChatClient
import atexit

chat_client = ChatClient()
atexit.register(chat_client.disconnect)