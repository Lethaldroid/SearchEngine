import socket
from _thread import *
import front
import pickle

host = socket.gethostname()
print(socket.gethostbyname(host))
port = 95

def client_handler(connection):

    while True:
        results = []
        data = connection.recv(2048)
        query = data.decode('utf-8')
        front.searching(str(query),results)
        results = pickle.dumps(results)
        connection.send(results)
        print(results)
    connection.close()


def accept_connections(ServerSocket):
    Client, address = ServerSocket.accept()
    print('Connected to socket ---> ' + address[0] + ':' + str(address[1]))
    start_new_thread(client_handler, (Client, ))


def start_server(host, port):
    ServerSocket = socket.socket()
    try:
        ServerSocket.bind((socket.gethostbyname(host), port))
    except socket.error as e:
        print(str(e))
    print(f'\n\t** Server is listing on the port {port} **')
    ServerSocket.listen()

    while True:
        accept_connections(ServerSocket)


start_server(host, port)
