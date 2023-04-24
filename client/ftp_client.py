# ==============================================
# This file is ran second in another terminal
# 'python3 ftp_client.py' 
# ==============================================

import socket
import os

# Define host and port for server to connect to
HOST = '127.0.0.1'
PORT = 5000

COMMANDS = ['ls', 'get', 'put']

# Create data socket for transferring data files
def create_data_socket():
    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket.bind((HOST, 0))
    data_socket.listen(1)
    return data_socket

# Create client socket for commands and connect to server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

while True:
    # Send command to server
    command = input('> ')
    cmd_parts = command.split()

    # If command is ls, get, put it creates a data socket
    if cmd_parts[0] in COMMANDS:
        data_socket = create_data_socket()
        data_port = data_socket.getsockname()[1]
        cmd_parts.insert(1, str(data_port))
        command = ' '.join(cmd_parts)

    # Send command to server
    client_socket.sendall(command.encode('utf-8'))

    # If quit then break out of the loop then disconnect connection
    if cmd_parts[0] == 'quit':
        print("Successfully disconnected.")
        break

    # If not in command list then error message 
    elif cmd_parts[0] not in COMMANDS:
        response = client_socket.recv(1024).decode('utf-8')
        print(response)

    # If get then grab file from the server
    elif cmd_parts[0] == 'get':
        # Receive server response for file transfer status
        response = client_socket.recv(1024).decode('utf-8').strip()

        if response.startswith('File not found'):
            print(response)
        else:
            # Accept server connection for data channel
            server_data_socket, _ = data_socket.accept()

            # Handle data transfer
            filename = cmd_parts[2]
            with open(filename, 'wb') as f:
                while True:
                    chunk = server_data_socket.recv(1024)
                    if not chunk:
                        break
                    f.write(chunk)
            server_data_socket.close()
            print(response)

    else:
        # Accept server connection for data channel
        server_data_socket, _ = data_socket.accept()

        # Handle data transfer
        if cmd_parts[0] == 'ls':
            response = b''
            while True:
                data = server_data_socket.recv(1024)
                if not data:
                    break
                response += data

            response_str = response.decode('utf-8')
            print(response_str)

        # If put then client stores file into the server
        elif cmd_parts[0] == 'put':
            filename = cmd_parts[2]
            if os.path.exists(filename):
                client_socket.sendall("file exists".encode('utf-8'))
                with open(filename, 'rb') as f:
                    while True:
                        chunk = f.read(1024)
                        if not chunk:
                            break
                        server_data_socket.sendall(chunk)
                server_data_socket.close()

                # Receive server response for file transfer status
                response = client_socket.recv(1024).decode('utf-8').strip()
                print(response)

            else:
                client_socket.sendall("file not found".encode('utf-8'))
                # Receive server response for file transfer status
                response = client_socket.recv(1024).decode('utf-8').strip()
                print(response)

                server_data_socket.close()


# Close client socket
client_socket.close()
