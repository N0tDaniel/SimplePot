import socket
import time

def start_honeypot(port, service):
    host = '0.0.0.0' # bind to all available interfaces
    backlog = 5 # maximum number of queued connections

    # create a socket and bind it to the host and port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(backlog)

    while True:
        # accept incoming connections
        client_socket, client_address = server_socket.accept()
        print("Accepted connection from {}".format(client_address))

        # log the incoming connection data for analysis
        with open('log.txt', 'a') as log:
            log.write("Accepted connection from {}\n".format(client_address))

        # simulate a specific service
        if service == 'ftp':
            client_socket.sendall(b'220 Welcome to the FTP server\r\n')
            data = client_socket.recv(1024)
            client_socket.sendall(b'331 Password required for anonymous\r\n')
            data = client_socket.recv(1024)
            client_socket.sendall(b'230 Login successful\r\n')

        elif service == 'ssh':
            client_socket.sendall(b'SSH-2.0-OpenSSH_7.6p1 Ubuntu-4ubuntu0.3\r\n')
            data = client_socket.recv(1024)
            client_socket.sendall(b'SSH-2.0-OpenSSH_7.6p1 Ubuntu-4ubuntu0.3\r\n')

        # close the connection
        client_socket.close()

if __name__ == '__main__':
    start_honeypot(22, 'ssh')
    start_honeypot(21, 'ftp')
