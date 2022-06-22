# 中间人
# 先捕包，截获数据，然后向双方发送数据

import json
from scapy.all import sniff, wrpcap, Raw, IP, TCP


config = None
server_config = None


def init():
    with open("./config.json") as f:
        global config, server_config
        config = json.load(f)
        server_config = config['server']


def callback(packet):
    print(packet[IP].src)
    print(packet[TCP].payload)
    print(type(packet))


def main():
    # 先对端口进行一次过滤，9999这个端口不是很常见，所以放心过滤
    # sniff(
        # filter=f"src or dst port {server_config['port']}", prn=callback, count=10)
    sniff(
        filter=f"src or dst port 443", prn=callback, count=10)


if __name__ == '__main__':
    init()
    main()
