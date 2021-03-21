from Control.Constants import *
import socket
from requests import get,post
import json

class ComAgent:
    def __init__(self):
        self.local_addr, self.public_addr = self.resolveAddress()
        self.publishAddress()
        self.com_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = None
        if DEBUG: print("initiated successfully")

    def send(self,message):
        if DEBUG: print("sending",message)
        self.connection.sendall(json.dumps(message).encode())

    def publishAddress(self):
        addr = {"local_ip" : self.local_addr, "public_ip" : self.public_addr ,"port" : str(COMPORT)}
        response = post(update_url, data=addr).content.decode()
        if response == '200':
            response = post(get_addr_url, data=credentials)
            response = response.content.decode()
            if response == 'bad credentials':
                print(">>> Warnning: update failed, bad credentials")
            elif '400' in response:
                print(">>> Warnning: update failed\n",response)
            else:
                if DEBUG: print("published successfully ",response)
        else:
            print(">>> Warnning: update failed")


    def resolveAddress(self):
        #find your own address and router address
        local_addr = socket.gethostbyname(socket.gethostname())
        public_addr = get('https://api.ipify.org').text
        if DEBUG: print("local ip: ",local_addr," public ip: ",public_addr)
        return local_addr, public_addr

    def awaitConnection(self):
        HOST = ''
        PORT = COMPORT
        s = self.com_socket
        s.bind((HOST, PORT))
        s.listen(1)
        print('Waiting for connection...')
        conn, addr = s.accept()
        print('Connected by:', addr)
        self.connection = conn

    def terminate(self):
        self.send('terminate')
        self.com_socket.close()