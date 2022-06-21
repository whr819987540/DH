#2022.6.20
import socket
# 创建一个socket对象，默认TCP套接字
s = socket.socket()
# 绑定端口
s.bind(('0.0.0.0',9999))
# 监听端口
s.listen(10)
print("正在连接中……")

# 建立连接之后，持续等待连接
while 1:
    # 阻塞等待连接
    sock,addr = s.accept()
    print(sock,addr)
    # 一直保持发送和接收数据的状态
    while 1:
        text = sock.recv(1024)
        # 客户端发送的数据为空的无效数据
        if len(text.strip()) == 0:
            print("服务端接收到客户端的数据为空")
        elif text.decode() == "exit":
            print("客户端下线")
            break
        else:
            print("收到客户端发送的数据为：{}".format(text.decode()))
            content = input("请输入发送给客户端的信息：")
            # 返回服务端发送的信息
            sock.send(content.encode())
    sock.close()
