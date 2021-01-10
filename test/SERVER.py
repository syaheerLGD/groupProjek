import socket
import threading
import os
import tqdm

class Server:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.accept_connections()
    
    def accept_connections(self):
        ip = str(input('Enter ip address --> '))
        port = int(input('Enter desired port --> '))

        self.s.bind((ip,port))
        self.s.listen(100)

        print('Running on IP: '+ip)
        print('Running on port: '+str(port))

        while 1:
            c, addr = self.s.accept()
            print(c)
            
            threading.Thread(target=self.handle_client,args=(c,addr,)).start()

    def handle_client(self,c,addr):
        data = c.recv(1024).decode()
        filesize = os.path.getsize(data)
        if not os.path.exists(data):
            c.send("file-doesn't-exist".encode())

        else:
            c.send("file-exists".encode())
            progress = tqdm.tqdm(range(filesize),f"Sending {data}", unit="B", unit_scale=True, unit_divisor=1024)
            print('Sending',data)
            if data != '':
                file = open(data,'rb')
                data = file.read(1024)
                while data:
                    c.send(data)
                    data = file.read(1024)
                    progress.update(len(data))

                c.shutdown(socket.SHUT_RDWR)
                c.close()
                

server = Server()


       



