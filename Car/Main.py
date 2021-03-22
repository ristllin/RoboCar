import socket
from requests import get,post
from Constants import *
from MovementControl import MovementAgent
import json
from time import sleep

def resolveIP():
    response = post(get_addr_url, data=credentials)
    response = response.content.decode().replace("'",'"')
    print(response)
    connection_details = json.loads(response)
    return connection_details


def connect_to_control(connection_details,movement_agent):
    HOST = connection_details['local_ip']
    PORT = int(connection_details['port'])
    while True:
        try:
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
                        speed = int(data["speed"])
                        acc = int(data["acc"])
                        action = data["action"]
                        movement_agent.move(speed,acc,action)
        except Exception as e:
            print(">> connection crashed",e)
            sleep(5)
            print("reconnecting..")
            
def main():
    sleep(3)
    movement_agent = MovementAgent()
    connection_details = None
    while connection_details == None:
        try:
            connection_details = resolveIP()
        except Exception as e:
            print("failed to connect, retry in 5 seconds")
            sleep(5)
    connect_to_control(connection_details,movement_agent)



if __name__ == "__main__":
    main()