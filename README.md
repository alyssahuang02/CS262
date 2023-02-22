# CS262

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
1. Setup a new environment through `spec-file.txt`. Run `conda create --name <env> --file spec-file.txt`
2. Change the server address `SERVER` value in `commands.py` to the `hostname` of your server.

### Running the Server
1. Open a new terminal session
2. Navigate to `gRPC` folder through `cd gRPC`
3. Run `python3 run_chat_server.py`

### Running the Client
1. Open a new terminal session
2. Navigate to `gRPC` folder through `cd gRPC`
3. Run `python3 run_chat_client.py`
4. Follow the prompts provided to send and receive messages

## Running Tests
### Wire Protocol
1. Navigate to `wire_protocol` folder through `cd wire_protocol`
2. Run `pytest client_tests.py`
3. Run `pytest server_tests.py`

### gRPC
1. Navigate to `gRPC` folder through `cd gRPC`
2. Run `pytest client_tests.py`
3. Run `pytest server_tests.py`
