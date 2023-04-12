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
        # Send file list to client in chunks
        for i in range(0, len(file_list), 1024):
            data = file_list[i:i+1024]
            client_socket.sendall(data.encode('utf-8'))

        # Send empty string to signal end of file list
        client_socket.sendall(''.encode('utf-8'))    
        
    elif command.startswith('GET'):
        # Extract filename from command
        filename = command.split()[1]

        try:
            # Open file and send contents to client
            with open(filename, 'rb') as f:
                while True:
                    # Read file contents in chunks
                    chunk = f.read(1024)

                    if not chunk:
                        # End of file
                        break
                    client_socket.sendall(chunk)

        except FileNotFoundError:
            # Send error message if file does not exist
            error_msg = f'File {filename} not found'

            # Send error message to client in chunks
            for i in range(0, len(error_msg), 1024):
                chunk = error_msg[i:i+1024]
            client_socket.sendall(chunk.encode('utf-8'))
              

            # Send empty string to signal end of error message
            client_socket.sendall(''.encode('utf-8'))

    else:
        # Invalid command
        error_msg = f'Invalid command: {command}'
        for i in range(0, len(error_msg), 1024):
                chunk = error_msg[i:i+1024]
        client_socket.sendall(chunk.encode('utf-8'))

    # Close client socket
    client_socket.close()
