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
    control_socket, client_address = server_socket.accept()

    print(f'Accepted connection from {client_address}')

    while True:
        # Read client command
        command = control_socket.recv(1024).decode('utf-8').strip()
        cmd_parts = command.split()

        # Handle command
        if cmd_parts[0] == 'ls' or cmd_parts[0] == 'get' or cmd_parts[0] == 'put':
            data_port = int(cmd_parts[1])
            data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            data_socket.connect(('127.0.0.1', data_port))

            if cmd_parts[0] == 'ls':
                file_list = '\n'.join(os.listdir())
                for i in range(0, len(file_list), 1024):
                    data = file_list[i:i + 1024]
                    data_socket.sendall(data.encode('utf-8'))
                data_socket.sendall(''.encode('utf-8'))

            elif cmd_parts[0] == 'get':
                filename = cmd_parts[2]
                if os.path.isfile(filename):
                    success_msg = f'File {filename} found'
                    control_socket.sendall(success_msg.encode('utf-8'))

                    with open(filename, 'rb') as f:
                        while True:
                            chunk = f.read(1024)
                            if not chunk:
                                break
                            data_socket.sendall(chunk)
                    data_socket.sendall(''.encode('utf-8'))
                else:
                    error_msg = f'File not found: {filename}'
                    control_socket.sendall(error_msg.encode('utf-8'))

            elif cmd_parts[0] == 'put':
                filename = cmd_parts[2]
                file_status = control_socket.recv(1024).decode('utf-8').strip()
                if file_status == "file exists":
                    with open(filename, 'wb') as f:
                        while True:
                            chunk = data_socket.recv(1024)
                            if not chunk:
                                break
                            f.write(chunk)
                    success_msg = f'File {filename} uploaded successfully'
                    control_socket.sendall(success_msg.encode('utf-8'))
                else:
                    error_msg = f"File {filename} not found."
                    control_socket.sendall(error_msg.encode('utf-8'))

            data_socket.close()

        elif cmd_parts[0] == 'quit':
            print(f'Close connection from {client_address}')
            print(f'Server listening on {HOST}:{PORT}')
            control_socket.close()
            break

        else:
            error_msg = f'Invalid command: {command}'
            for i in range(0, len(error_msg), 1024):
                chunk = error_msg[i:i+1024]
            control_socket.sendall(chunk.encode('utf-8'))

    control_socket.close()

server_socket.close()
