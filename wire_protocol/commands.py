# Connection Data
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
# SERVER = "dhcp-10-250-18-31.harvard.edu" # TODO: need to change later/have some way to make it dynamic
SERVER = "Alyssas-MBP.wireless.yale.internal"
ADDR = (SERVER, PORT)

# Data Types
PURPOSE = "!PURPOSE:"
RECIPIENT = "!RECIPIENT:"
SENDER = "!SENDER:"
LENGTH = "!LENGTH:"
BODY = "!BODY:"

# General
SEPARATOR = "/"
MAX_BANDWIDTH = 2048 # TODO: WE HAVE TO CHECK STUFF DOES NOT EXCEED THIS

# Client Purposes
CHECK_USER_EXISTS = "!CHECKUSEREXISTS"
DELETE_ACCOUNT = "!DELETEACCOUNT"
SHOW_ACCOUNTS = "!SHOWACCOUNTS"
LOGIN = "!LOGIN"
REGISTER = "!REGISTER"
PULL_MESSAGE = "!PULL"
SEND_MESSAGE = "!SEND"
LOGOUT = "!LOGOUT"

# Server Purposes
NO_MORE_DATA = "!NOMOREDATA"
NOTIFY = "!NOTIFY"

# Printable messages from NOTIFY
LOGIN_SUCCESSFUL = "Login successful!"
USER_DOES_NOT_EXIST = "User does not exist."
DELETION_SUCCESSFUL = "Account deleted."
LOGOUT_SUCCESSFUL = "Logging out."