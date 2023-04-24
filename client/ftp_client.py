import socket
import os

# Define host and port for server to connect to
HOST = '127.0.0.1'
PORT = 5000

def create_data_socket():
    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket.bind((HOST, 0))
    data_socket.listen(1)
    return data_socket

# Create client socket and connect to server
control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
control_socket.connect((HOST, PORT))

while True:
    # Send command to server
    command = input('> ')
    cmd_parts = command.split()
    if cmd_parts[0] in ['ls', 'get', 'put']:
        data_socket = create_data_socket()
        data_port = data_socket.getsockname()[1]
        cmd_parts.insert(1, str(data_port))
        command = ' '.join(cmd_parts)

    control_socket.sendall(command.encode('utf-8'))

    if cmd_parts[0] == 'quit':
        print("Successfully disconnected.")
        break
    elif cmd_parts[0] not in ['ls', 'get', 'put']:
        response = control_socket.recv(1024).decode('utf-8')
        print(response)
    elif cmd_parts[0] == 'get':
        # Receive server response for file transfer status
        response = control_socket.recv(1024).decode('utf-8').strip()

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

        elif cmd_parts[0] == 'put':
            filename = cmd_parts[2]
            if os.path.exists(filename):
                control_socket.sendall("file exists".encode('utf-8'))
                with open(filename, 'rb') as f:
                    while True:
                        chunk = f.read(1024)
                        if not chunk:
                            break
                        server_data_socket.sendall(chunk)
                server_data_socket.close()

                # Receive server response for file transfer status
                response = control_socket.recv(1024).decode('utf-8').strip()
                print(response)
            else:
                control_socket.sendall("file not found".encode('utf-8'))
                print(f"File {filename} not found.")
                server_data_socket.close()


# Close control socket
control_socket.close()
