import socket
import select


class Client:
    def __init__(self, host='127.0.0.1', port=8080):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = host, port


    def connect(self):
        self.sock.connect(self.address)

    def disconnect(self):
        self.sock.close()

    def send(self, msg: str):
        sent = self.sock.send(msg.encode())
        if sent == 0:
            raise RuntimeError('Socket connection broken')


    def receive(self):
        received_msg = self.sock.recv(64).decode()
        if received_msg == '':
            raise RuntimeError('Socket connection broken')

        return received_msg


client = Client()
client.connect()
msg = 'Testing sending from client to server'
print('[SENT FROM CLIENT]: ' + msg)
client.send(msg)
recv = client.receive()
print('[RECEIVED FROM SERVER]: ' + recv)
client.disconnect()

