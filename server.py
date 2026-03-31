import socket
import threading

HOST = "0.0.0.0"
PORT = 5555

clients = []

def broadcast(message, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(message)
            except:
                clients.remove(client)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message, client)
        except:
            clients.remove(client)
            client.close()
            break

def start():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print("Server running...")

    while True:
        client, addr = server.accept()
        print("Connected:", addr)
        clients.append(client)

        threading.Thread(target=handle_client, args=(client,)).start()

start()