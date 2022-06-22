
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
    p,g = data['p'],data['g']
    # 生成私钥b，公钥B
    b = get_private_key(p)
    B = get_public_key(p,g,b)
    data = {
        "server_public_key":B
    }
    # server B -> client
    connect_socket.send(json.dumps(data).encode())
    # client A -> server
    data = json.loads(connect_socket.recv(server_config['bufsize']).decode())
    A = data['client_public_key']
    
    S = get_S(p,b,A)
    print(f"p = {p}, g = {g}")
    print(f"[CLEINT] public_key = {A}")
    print(f"[SERVER] private_key = {b}, public_key = {B}")
    print(f"[DH] S = {S}")
    
    connect_socket.close()


if __name__ == "__main__":
    init()
    main()

    # # 建立连接之后，持续等待连接
    # while 1:
    #     # 阻塞等待连接
    #     sock,addr = s.accept()
    #     print(sock,addr)
    #     # 一直保持发送和接收数据的状态
    #     while 1:
    #         text = sock.recv(1024)
    #         # 客户端发送的数据为空的无效数据
    #         if len(text.strip()) == 0:
    #             print("服务端接收到客户端的数据为空")
    #         elif text.decode() == "exit":
    #             print("客户端下线")
    #             break
    #         else:
    #             print("收到客户端发送的数据为：{}".format(text.decode()))
    #             content = input("请输入发送给客户端的信息：")
    #             # 返回服务端发送的信息
    #             sock.send(content.encode())
    #     sock.close()
