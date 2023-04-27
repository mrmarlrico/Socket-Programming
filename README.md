# CPSC471 - Socket Programming

## Members:
* Kevin Sierras: armyoffreaks123@csu.fullerton.edu
* Marl Rico: mrmarlrico@csu.fullerton.edu
* Anahid Zandi Haghighi: anazandi@csu.fullerton.edu
* Parth Sharma: parthsharma@csu.fullerton.edu
* Tina Duong: 

## Project Description:
This is a simple FTP server/client program. The client connects to the server and it can use simple commands to interact with the server itself.

## How to use:
**You will need to update your python if any error pertaining to python emerge.**

> On one terminal, execute `"ftp_server.py"` using this command: 
* `"python ftp_server.py"` or `"python3 ftp_server.py"`

> On another terminal, execute `"ftp_client.py"` using this command:
* `"python ftp_client.py"` or `"python3 ftp_client.py"`
* Wait for a confirmation server side

> Once connected, you can interact with the server on the client side using these commands: 
* ls: this will list out all the files on the server
* get [filename] : this will retrieve the specified file on the server
* put [filename] : this will insert a file from the client side to the server
* quit: this will close the client and server side connections
