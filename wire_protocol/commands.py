# Connection Data
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
## Edit Server below to the hostname of the machine running the server
SERVER = "dhcp-10-250-18-31.harvard.edu"
ADDR = (SERVER, PORT)

# Data Types
PURPOSE = "!PURPOSE:"
RECIPIENT = "!RECIPIENT:"
SENDER = "!SENDER:"
LENGTH = "!LENGTH:"
BODY = "!BODY:"

# General
SEPARATOR = "/"
MAX_BANDWIDTH = 2048

# Client Purposes
CHECK_USER_EXISTS = "!CHECKUSEREXISTS"
DELETE_ACCOUNT = "!DELETEACCOUNT"
SHOW_ACCOUNTS = "!SHOWACCOUNTS"
LOGIN = "!LOGIN"
REGISTER = "!REGISTER"
PULL_MESSAGE = "!PULL"
SEND_MESSAGE = "!SEND"
LOGOUT = "!LOGOUT"
DISCONNECT = "!DISCONNECT"

# Server Purposes
NO_MORE_DATA = "!NOMOREDATA"
NOTIFY = "!NOTIFY"

# Printable messages from NOTIFY
LOGIN_SUCCESSFUL = "Login successful!"
USER_DOES_NOT_EXIST = "No users found. Try again."
DELETION_SUCCESSFUL = "Account deleted."
LOGOUT_SUCCESSFUL = "Logging out."