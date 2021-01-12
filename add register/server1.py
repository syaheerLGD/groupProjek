import os
import sys
import threading
import socket
import tqdm
import time
from cryptography.fernet import Fernet

def encryp(filename,key):
    f = Fernet(key)

def animation(msg):
        for char in msg:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(0.1)

class Server:
    start = '\t\tWelcome To Secure File Transfer\n'
    animation(start)
    print('-------------------------------------------------------------------')
    numIp = '\tServer IP : 192.168.0.200\n'
    animation(numIp)
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.Terima_connections()

    def Terima_connections(self):
        ip = str(input('\tEnter Ip Address Of Your Server : '))
        port = int(input('\tEnter Desired Port Number : '))

        self.sock.bind((ip,port))
        self.sock.listen(100)
        print('\n')

        while 1:
            c, addr = self.sock.accept()
            print('\tConnected to :' + addr[0])

            threading.Thread(target=self.handle_client,args=(c,addr,)).start()
            
    def handle_client(self,c,addr):
        New = c.recv(1024)
        if New.decode() == "y":
            with open("login.txt", "a+") as register:
                use = c.recv(1024).decode()
                pas = c.recv(1024).decode()
                register.seek(0)
                register.write(use)
                register.write(":")
                register.write(pas)
                register.write('\n')
                c.send("continue".encode())

            with open("login.txt", "r") as login:
                username = c.recv(1024).decode()
                password = c.recv(1024).decode()

                jumpa = "tak jumpa";
                for line in login:
                    creds = line.strip()
                    if creds.split(":")[0] in username and creds.split(":")[1] in password:
                        jumpa = "jumpa";

                if jumpa == "jumpa":
                    c.send(("\tWelcome New User : %s" % (username)).encode())
                else:
                    c.send("Not-a-user".encode())
                    #c.close()
        else:
            with open("login.txt", "r") as login:
                username = c.recv(1024).decode()
                password = c.recv(1024).decode()

                jumpa = "tak jumpa";
                for line in login:
                    creds = line.strip()
                    if creds.split(":")[0] in username and creds.split(":")[1] in password:
                        jumpa = "jumpa";

                if jumpa == "jumpa":
                    c.send(("\tWelcome back: %s" % (username)).encode())
                else:
                    c.send("Not-a-user".encode())
                    #c.close()

        while 1:
            data = c.recv(1024).decode()
            if not os.path.exists(data):
                c.send("File Doesn't Exist In The Server".encode())
                continue
            else:
                c.send("File Exist".encode())
                print('\tSending',data)
                if data != '':
                    file = open(data,'rb')
                    data = file.read(1024)
                    #encrypted_data = f.encrypt(data)
                    while data:
                        c.send(data)
                        data = file.read(1024)
                continue
               #c.shutdown(socket.SHUT_RDWR)
               #c.close()

        #c.shutdown(socket.SHUT_RDWR)
        #c.close()

server = Server()
