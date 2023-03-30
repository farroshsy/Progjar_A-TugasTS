import os
import socket
import threading
import time
import logging
import ssl
from http import HttpServer
from multiprocessing import Process

httpserver = HttpServer()

class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)

    def run(self):
        rcv=""
        while True:
            try:
                data = self.connection.recv(32)
                if data:
                    #merubah input dari socket (berupa bytes) ke dalam string
                    #agar bisa mendeteksi \r\n
                    d = data.decode()
                    rcv=rcv+d
                    if rcv[-2:]=='\r\n':
                        #end of command, proses string
                        logging.warning("data dari client: {}" . format(rcv))
                        hasil = httpserver.proses(rcv)
                        #hasil akan berupa bytes
                        #untuk bisa ditambahi dengan string, maka string harus di encode
                        hasil=hasil+"\r\n\r\n".encode()
                        logging.warning("balas ke  client: {}" . format(hasil))
                        #hasil sudah dalam bentuk bytes
                        self.connection.sendall(hasil)
                        rcv=""
                        self.connection.close()
                else:
                    break
            except OSError as e:
                pass
        self.connection.close()

def run_server():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.bind(('0.0.0.0', 8899))
    my_socket.listen(1)
    while True:
        connection, client_address = my_socket.accept()
        try:
            clt = ProcessTheClient(connection, client_address)
            clt.start()
        except:
            logging.exception("Error: ")
    connection.close()

if __name__ == "__main__":
    run_server()
