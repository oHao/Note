# 向指定IP/端口发送数据并打印接收到的信息
from socket import *

HOST = 'localhost'
PORT = 8082
BUFSIZ = 1024
ADDR = (HOST,PORT)

tcpClisock = socket(AF_INET,SOCK_STREAM)
tcpClisock.connect(ADDR)
while True:
    data = input('> ')
    if not data:
        break
    tcpClisock.send(bytes(data,'utf-8'))
    data = tcpClisock.recv(BUFSIZ).decode()
    print(type(data))
    if not data:
        break
    print(data)
tcpClisock.close()
