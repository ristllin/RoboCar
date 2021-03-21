import socket
from requests import get,post
from Car.Constants import *
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
                data = s.recv(1024)
                print('Received', repr(data))
                if '"terminate"' == data.decode() or '' == data.decode():
                    s.close()
                    break

def main():
    connection_details = resolveIP()
    connect_to_control(connection_details)



if __name__ == "__main__":
    main()