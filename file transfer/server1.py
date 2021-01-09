import os
import threading
import socket
from _thread import *
import tqdm

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096
#ThreadCount = 0
class Server:
    print('\t\tWelcome To Secure File Transfer')
    print('-------------------------------------------------------------------')
    print('Server IP : 192.168.1.11') 
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.accept_connections()
    
    def accept_connections(self):
        ip = str(input('Enter Ip Address Of Your Server : '))
        port = int(input('Enter Desired Port Number : '))

        self.sock.bind((ip,port))
        self.sock.listen(100)
        print('\n')

        print('Socket Connect to IP : '+ip)
        print('Socket Connect to port : '+str(port))

        while 1:
            c, addr = self.sock.accept()
#            print(c)

            threading.Thread(target=self.handle_client,args=(c,addr,)).start()

    def handle_client(self,c,addr):
        data = c.recv(1024).decode()
        filesize = os.path.getsize(data)
        progress = tqdm.tqdm(range(filesize), f"sending {data}", unit="B", unit_scale=True, unit_divisor=1024)
    
        if not os.path.exists(data):
            c.send("file doesn't exist in the server".encode())

        else:
            with open(data, "rb") as f:
               c.send(f"{data}{SEPARATOR}{filesize}".encode())
               print('Sending',data)
               if data != '':
               # file = open(data,'rb')
                  data = f.read(BUFFER_SIZE)
                  while data:
                     c.send(data)
                     progress.update(len(data))
                     data = f.read(1024)

                     c.shutdown(socket.SHUT_RDWR)
                     c.close()
                

server = Server()
