import socket
import os
import tqdm

BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
class Client:
    print('\t\tWelcome To Secure File Transfer')
    print('-------------------------------------------------------------------')
    print('Client') 
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.connect_to_server()

    def connect_to_server(self):
        self.target_ip = input(str('Enter Ip Address : '))
        self.target_port = input('Enter Port Number : ')

        self.sock.connect((self.target_ip,int(self.target_port)))

        self.main()

    def reconnect(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect((self.target_ip,int(self.target_port)))

    def main(self):
        while 1:
            file_name = input('Enter File Name On Server : ')
            self.sock.send(file_name.encode())

            confirmation = self.sock.recv(BUFFER_SIZE).decode()
            if confirmation == "file-doesn't-exist":
                print("File doesn't exist on server.")

                self.sock.shutdown(socket.SHUT_RDWR)
                self.sock.close()
                self.reconnect()

            else:        
                write_name = file_name
                file_name, filesize = confirmation.split(SEPARATOR)
                file_name = os.path.basename(file_name)
                filesize = int(filesize)
                progress = tqdm.tqdm(range(filesize), "Receiving {file_name}", unit="B", unit_scale=True, unit_divisor=1024)
                if os.path.exists(write_name): os.remove(write_name)

                with open(write_name,'wb') as file:
                    while 1:
                        data = self.sock.recv(BUFFER_SIZE)
                        data = self.sock.read(BUFFER_SIZE)
                        if not data:
                            break

                        file.write(data)
                progress.update(len(data))
                print(file_name,'Successfully Downloaded.\n')

                self.sock.shutdown(socket.SHUT_RDWR)
                self.sock.close()
                self.reconnect()
                
client = Client()
