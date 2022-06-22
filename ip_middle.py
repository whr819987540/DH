# 中间人
# 先捕包，截获数据，然后向双方发送数据

from itertools import count
import os
from scapy.all import sniff,wrpcap,Raw,IP,TCP







def func(packet):
    print(type(packet))
    
def main():
    sniff(filter="src or dst port 443",prn=func,count=0)


if __name__ =='__main__':
    main()
