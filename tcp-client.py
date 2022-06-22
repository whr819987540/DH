
import socket
from random import randint
import json
from func import *


config = None
server_config = None


def init():
    with open("./config.json") as f:
        global config, server_config
        config = json.load(f)
        server_config = config['server']
        
def get_local_ip():
    return socket.gethostbyname(socket.gethostname())



def main():
    connect_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
    connect_socket.connect((get_local_ip(),server_config['port']))
    
    # 生成大素数p
    p = generate_big_prime()
    # 原根g
    g = get_big_prime_generator(p)
    # client p/g -> server
    data = {
        "p":p,
        "g":g
    }
    connect_socket.send(json.dumps(data).encode())
    # 生成私钥a，公钥A
    a = get_private_key(p)
    A = get_public_key(p,g,a)
    # server B -> client
    data = json.loads(connect_socket.recv(server_config['bufsize']).decode())
    B = data['server_public_key']
    # client A -> server
    data = {
        "client_public_key":A
    }
    connect_socket.send(json.dumps(data).encode())
    
    S = get_S(p,a,B)
    print(f"p = {p}, g = {g}")
    print(f"[CLEINT] private_key = {a}, public_key = {A}")
    print(f"[SERVER] public_key = {B}")
    print(f"[DH] S = {S}")
    
    connect_socket.close()
    
    
    
if __name__ == "__main__":
    init()
    main()

    # 创建一个socket对象
    s1 = socket.socket()
    s1.connect(('10.236.197.1',9999))
    # 不断发送和接收数据
    while 1:
        send_data = input("客户端要发送的信息：")
        # socket传递的都是bytes类型的数据,需要转换一下
        if send_data=="exit":
            info="exit"
            s1.send(info.encode())
            break
        else:
            s1.send(send_data.encode())
            # 接收数据，最大字节数1024,对返回的二进制数据进行解码
            text = s1.recv(1024).decode()
            print("服务端发送的数据：{}".format(text))
            print("------------------------------")
