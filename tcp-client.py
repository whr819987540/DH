
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
    connect_socket.connect((server_config['server_ip'],server_config['port']))
    
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
    
    # 计算对称秘钥
    S = get_S(p,a,B)
    print(f"p = {p}, g = {g}")
    print(f"[CLEINT] private_key = {a}, public_key = {A}")
    print(f"[SERVER] public_key = {B}")
    print(f"[DH] S = {S}")
    
    # 传输内容
    data = "hello world"
    # AES256-GCM加密
    encrypt_data = AES256_GCM_encrypt()
    # 发送加密数据
    data = {
        "msg":encrypt_data
    }
    connect_socket.send(json.dumps(data).encode())
    
    connect_socket.close()
    
    
if __name__ == "__main__":
    init()
    main()
