# CS262

## Wire Protocol
- 1.5 message case - client not receiving properly
- Printing situation:
  - Login successful printed 4 times (should be fixed - alyssa)
  - Normal message delivery printed 2 times (should be fixed - alyssa)
  - Then messages maybe(?) resent after a user logs back in when disconnected (should be fixed - alyssa)
- Disconnect login again as same person and it hangs(?)
- General disconnect handling (done on wire; is this done on grpc??)
- Change prompt for deletion - "Enter 0 to delete, enter anything else if not." (done)
- List accounts (done)
- Two people logging in to the same account from different laptops (done just errors out)
- Make regex consistent across grpc and wires

Build this in a repo on github that you make publicly available. The repo should include a README file that gives a set of instructions on setting up the client and server so that the system can be run. Part of your grade will depend on how well the code that you provide is documented. You may write you client and server in any of (or any combination of) python, C, C++, Java, or C#. Any other language requires the explicit permission of the instructor, which you won't get. Keep a notebook for what decisions you made, and why you made them the way you did, and any interesting observations that come up along the way.

## Wire Protocol
### Setup
1. Setup a new environment through `spec-file.txt`. Run `conda create --name <env> --file spec-file.txt`
2. Change the server address `SERVER` value in `commands.py` to the `hostname` of your server.

### Running the Server
1. Open a new terminal session
2. Navigate to `wire_protocol` folder through `cd wire_protocol`
3. Run `python3 run_chat_server.py`

### Running the Client
1. Open a new terminal session
2. Navigate to `wire_protocol` through `cd wire_protocol`
3. Run `python3 run_chat_client.py`
4. Follow the prompts provided to send and receive messages

## gRPC
### Setup
1. Setup a new environment through `requirements.txt`
3. Change the server address `SERVER` value in `commands.py` to the `hostname` of your server.

### Running the Server

### Running the Client

- install grpcio
- install google-api-python-client
