import socket
import os

class Client:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.connect_to_server()

    def connect_to_server(self):
        self.target_ip = input(str('Enter ip --> '))
        self.target_port = input('Enter port --> ')

        self.s.connect((self.target_ip,int(self.target_port)))

        self.main()

    def reconnect(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.connect((self.target_ip,int(self.target_port)))

    def main(self):
        username = input('Username: ')
        self.s.send(username.encode())
        password = input('Password: ')
        self.s.send(password.encode())

        login = self.s.recv(1024)
        if login.decode() == "Not-a-user":
            print("Not a user. Connection will be terminate.")
            self.s.shutdown(socket.SHUT_RDWR)
            self.s.close()
        else:
            print(login.decode())

        print("Enter 'exit' to terminate connection.")
        while 1:
            file_name = input('Enter file name on server --> ')
            if file_name == "exit":
                self.s.shutdown(socket.SHUT_RDWR)
                self.s.close()
            else:
                self.s.send(file_name.encode())
    
            confirmation = self.s.recv(1024)
            if confirmation.decode() == "file-doesn't-exist":
                print("File doesn't exist on server.")

                self.s.shutdown(socket.SHUT_RDWR)
                self.s.close()
                self.reconnect()

            else:
                write_name = 'from_server '+file_name
                if os.path.exists(write_name): os.remove(write_name)

                with open(write_name,'wb') as file:
                    while 1:
                        data = self.s.recv(1024)

                        if not data:
                            break

                        file.write(data)

                print(file_name,'successfully downloaded.')

                self.s.shutdown(socket.SHUT_RDWR)
                self.s.close()
                self.reconnect()

client = Client()
