import socket
import select
import time

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '127.0.0.1'
port = 8080

server_sock.bind((host, port))

server_sock.listen(5)

print("Started listening for connections")

while True:
    client_sock, addr = server_sock.accept()
    print("Connected")

    r, _, _ = select.select([client_sock], [], [], 0)

    if r:
        print('There is data to be read on the server side client')
    else:
        print('There is not data to be read on the server side client')

    chunk = client_sock.recv(4096).decode()
    print('[RECEIVED FROM CLIENT]: ' + chunk)



    msg = 'Thanks for connecting to this server!'
    print('[SENT FROM SERVER]: ' + msg)
    sent = client_sock.send(msg.encode())
    print(f'Sent value: {sent}')
    client_sock.close()
    break

server_sock.close()