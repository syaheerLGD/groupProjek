import socket
import threading
import os

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
        with open("login.txt", "r") as login:
            username = c.recv(1024).decode()
            password = c.recv(1024).decode()

            jumpa = "tak jumpa";
            for line in login:
                creds = line.strip()
                if creds.split(":")[0] in username and creds.split(":")[1] in password:
                    jumpa = "jumpa";

            if jumpa == "jumpa":
                c.send(("Welcome back: %s" % (username)).encode())
            else:
                c.send("Not-a-user".encode())
                #c.close()

        data = c.recv(1024).decode()
        
        if not os.path.exists(data):
            c.send("file-doesn't-exist".encode())

        else:
            c.send("file-exists".encode())
            print('Sending',data)
            if data != '':
                file = open(data,'rb')
                data = file.read(1024)
                while data:
                    c.send(data)
                    data = file.read(1024)

                c.shutdown(socket.SHUT_RDWR)
                c.close()


server = Server()
