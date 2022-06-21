#2022.6.20
import socket
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
