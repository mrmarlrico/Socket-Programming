# ==============================================
# This file is ran second in another terminal
# 'python3 ftp_client.py' 
# ==============================================

import socket

# Define host and port for server to connect to
HOST = '127.0.0.1'
PORT = 5000

# Create client socket and connect to server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

while True:
    # Send command to server
    command = input('> ')
    client_socket.sendall(command.encode('utf-8'))

    # Receive response from server
    response = client_socket.recv(1024).decode('utf-8')

    # Print response to console
    print(response)

# Close client socket
client_socket.close()