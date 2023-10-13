#!/usr/bin/python3

import socket
import threading
import ssl


class Server:
    def __init__(self):
        self.ip = socket.gethostbyname(socket.gethostname())
        while 1:
            try:
                self.port = 9060

                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.s.bind((self.ip, self.port))
                self.s.listen(100)

                # Wrap the socket with SSL
                self.s = ssl.wrap_socket(self.s,
                                         server_side=True,
                                         certfile='ssl_certs_keys/certificate.pem',
                                         keyfile='ssl_certs_keys/key.pem')

                break
            except:
                print("Couldn't bind to that port")

        self.connections = []
        self.accept_connections()

    def accept_connections(self):
        print('Running on IP: ' + self.ip)
        print('Running on port: ' + str(self.port))

        while True:
            c, addr = self.s.accept()

            self.connections.append(c)

            threading.Thread(target=self.handle_client, args=(c, addr,)).start()

    def broadcast(self, sock, data):
        for client in self.connections:
            if client != self.s and client != sock:
                try:
                    client.send(data)
                except ssl.SSLError as e:
                    print("Broadcast SSL error: ", e)
                    if client in self.connections:
                        self.connections.remove(client)
                        break
                except socket.error as e:
                    print("Broadcast socket error: ", e)
                    if client in self.connections:
                        self.connections.remove(client)
                        break


    def handle_client(self, c, addr):
        while True:
            try:
                data = c.recv(1024)
                if not data:
                    break
                self.broadcast(c, data)

            except Exception as e:
                print(f"Handle client exception: {e}")
                c.close()
                if c in self.connections:
                    self.connections.remove(c)
                break

server = Server()