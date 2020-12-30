import socket
import os
from _thread import*

s = socket.socket()
ip = input(str("Please enter the host address of the server: "))
port = 8000
s.connect((ip,port))
print("Connected ...\n")

respons = s.recv(1024)
print(respons)

Input = input('\nPlease enter the name file that you want: ')
s.send(str.encode(Input))
response = s.recv(1024)
print(response.decode('utf-8'))


filename = input(str("\nPlease enter a filename for the incoming file: "))
file = open(filename, 'wb')
file_data = s.recv(1024)
file.write(file_data)
file.close()
print("File has been received succesfully.\n")

s.close()
