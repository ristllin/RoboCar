import socket
from requests import get,post
from Car.Constants import *
from Car.MovementControl import move
import json
from time import sleep

def resolveIP():
    response = post(get_addr_url, data=credentials)
    response = response.content.decode().replace("'",'"')
    print(response)
    connection_details = json.loads(response)
    return connection_details


def connect_to_control(connection_details):
    HOST = connection_details['local_ip']
    PORT = int(connection_details['port'])
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((HOST, PORT))
                print(">>> Connection established")
            except Exception as e:
                print(">>> Connection failed, 10 sec timeout...")
                sleep(10)
                continue
            while True:
                raw_data = s.recv(1024).decode()
                data = json.loads(raw_data)
                print('Received', repr(raw_data))
                if '"terminate"' == raw_data or '' == raw_data:
                    s.close()
                    break
                else:
                    move(data["speed"],data["acc"],data["action"])

def main():
    connection_details = resolveIP()
    connect_to_control(connection_details)



if __name__ == "__main__":
    main()