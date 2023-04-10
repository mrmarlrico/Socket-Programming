# ============================================================
# This file is ran first in one terminal
# 'python3 ftp_server.py' 
# ============================================================

import socket
import os

# Define host and port for server to listen on
HOST = '127.0.0.1'
PORT = 5000

# Create server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f'Server listening on {HOST}:{PORT}')

while True:
    # Accept incoming client connection
    client_socket, client_address = server_socket.accept()

    print(f'Accepted connection from {client_address}')

    # Read client command
    command = client_socket.recv(1024).decode('utf-8').strip()

    # Handle command
    if command == 'LIST':
        # Send list of files in current directory to client
        file_list = '\n'.join(os.listdir())
        client_socket.sendall(file_list.encode('utf-8'))
    elif command.startswith('GET'):
        # Extract filename from command
        filename = command.split()[1]

        try:
            # Open file and send contents to client
            with open(filename, 'rb') as f:
                file_contents = f.read()
                client_socket.sendall(file_contents)
        except FileNotFoundError:
            # Send error message if file does not exist
            error_msg = f'File {filename} not found'
            client_socket.sendall(error_msg.encode('utf-8'))
    elif command == 'quit':
        client_socket.close()

    # Close client socket
    client_socket.close()