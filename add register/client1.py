import socket
import os
import tqdm
import time
import sys

def encrpyt(file_name,key):
     f = Fernet(key)

def animation(msg):
        for char in msg:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(0.1)

#BUFFER_SIZE = 4096
#SEPARATOR = "<SEPARATOR>"
class Client:
    start = '\t\tWelcome To Secure File Transfer\n'
    animation(start)
    print('-------------------------------------------------------------------')
    cl = '\tClient\n'
    animation(cl)
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.connect_to_server()

    def connect_to_server(self):
        self.target_ip = input(str('\tPlease Enter Ip Address : '))
        self.target_port = input('\tPlease Enter Port Number : ')

        self.sock.connect((self.target_ip,int(self.target_port)))

        self.main()

    def reconnect(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect((self.target_ip,int(self.target_port)))

    def main(self):
        New = input('\tAre you a new user?(y/n) :')
        self.sock.send(New.encode())
        if New == 'y':
            use = input('\tUsername :')
            self.sock.send(use.encode())
            pas = input('\tPassword :')
            self.sock.send(pas.encode())
            register = self.sock.recv(1024)
            if register.decode() == "continue":
                print('\t\t%Login Again%')
                username = input('\tUsername: ')
                self.sock.send(username.encode())
                password = input('\tPassword: ')
                self.sock.send(password.encode())

                login = self.sock.recv(1024)
                if login.decode() == "Not-a-user":
                    print("\tNot a user. Connection will be terminate.")
                    self.sock.shutdown(socket.SHUT_RDWR)
                    self.sock.close()
                    sys.exit()
                else:
                    print(login.decode())
        else:
            print('\t\t%Login%')
            username = input('\tUsername: ')
            self.sock.send(username.encode())
            password = input('\tPassword: ')
            self.sock.send(password.encode())

            login = self.sock.recv(1024)
            if login.decode() == "Not-a-user":
                print("\tNot a user. Connection will be terminate.")
                self.sock.shutdown(socket.SHUT_RDWR)
                self.sock.close()
                sys.exit()
            else:
                print(login.decode())
		
        print("\t|Enter 'exit' To Terminate Connection.| ")
        while 1:
            file_name = input('\tPlease Enter File Name On Server : ')
            if file_name == "exit":
                #self.sock.shutdown(socket.SHUT_RWDR)
                #self.sock.close()
                sys.exit()

            else:
                self.sock.send(file_name.encode())

            confirm = self.sock.recv(1024)
            if confirm.decode() == "File Doesn't Exist In The Server":
                exist = "\tFile Doesn't Exist At Server.\n"
                animation(exist)
                continue
                #self.sock.shutdown(socket.SHUT_RDWR)
                #self.sock.close()
                #self.reconnect()

            else:
                write_name = file_name
                if os.path.exists(write_name): os.remove(write_name)

                with open(write_name,'wb') as file:
                    while 1:
                        data = self.sock.recv(1024)

                        if not data:
                            break

                        file.write(data)
                        break

                success = '\tFile Successfully Downloaded.\n'
                animation(success)
                continue

                #self.sock.shutdown(socket.SHUT_RDWR)
                #self.sock.close()
                #self.reconnect()

client = Client()
