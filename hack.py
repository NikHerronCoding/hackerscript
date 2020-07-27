# write your code here
import socket
import pdb
import sys
import string
import itertools
char_bank = string.ascii_lowercase + string.digits


ip_address, port = sys.argv[1], int(sys.argv[2])
hacker_socket = socket.socket()

address = (ip_address, port)
hacker_socket.connect(address)
response = ''
num_chars = 1

password_generator = itertools.product(char_bank, repeat=num_chars)

while response != 'Connection success!':
    if response == 'Too many attempts to connect!':
        response = 'Password crack fail'
        break
    try:
        password = next(password_generator)
    except StopIteration:
        if num_chars == 4:
            break
        num_chars += 1
        password_generator = itertools.product(char_bank, repeat=num_chars)
        password = next(password_generator)
    hacker_socket.send(''.join(password).encode('utf8'))
    byte_response = hacker_socket.recv(1024)
    response = byte_response.decode('utf8')

hacker_socket.close()
print(''.join(password))








