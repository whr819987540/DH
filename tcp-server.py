
import socket
import json
from threading import Thread
from func import *

config = None
server_config = None


def init():
    with open("./config.json") as f:
        global config, server_config
        config = json.load(f)
        server_config = config['server']


def main():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    print((server_config['ip'], server_config['port']))
    listen_socket.bind((server_config['ip'], server_config['port']))
    listen_socket.listen(5)

    while input("input q to quit, other to continue ...\n") != 'q':
        connect_socket, addr = listen_socket.accept()
        print(f"[CONNECT] {addr}")
        t = Thread(target=serve, args=[connect_socket])
        t.start()


def serve(connect_socket: socket.socket):
    # client p/g -> server
    data = json.loads(connect_socket.recv(server_config['bufsize']).decode())
    p, g = data['p'], data['g']
    # 生成私钥b，公钥B
    b = get_private_key(p)
    B = get_public_key(p, g, b)
    data = {
        "server_public_key": B
    }
    # server B -> client
    connect_socket.send(json.dumps(data).encode())
    # client A -> server
    data = json.loads(connect_socket.recv(server_config['bufsize']).decode())
    A = data['client_public_key']

    # 计算对称秘钥S
    S = get_S(p, b, A)
    print(f"p = {p}, g = {g}")
    print(f"[CLEINT] public_key = {A}")
    print(f"[SERVER] private_key = {b}, public_key = {B}")
    print(f"[DH] S = {S}")

    # 接收加密数据
    data = json.loads(connect_socket.recv(server_config['bufsize']).decode())['msg']
    # AES256-GCM解密
    # decrypt_data = AES256_GCM_decrypt()
    decrypt_data = data
    print(decrypt_data)

    connect_socket.close()


if __name__ == "__main__":
    init()
    main()
    