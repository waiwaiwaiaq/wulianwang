from socket import *
import time
import json
import numpy as np
import random

# TCP协议传输通道
tcp_socket = socket(AF_INET, SOCK_STREAM)
# 连接服务器
serve_ip = "100.78.183.195"
serve_port = 8081
tcp_socket.connect((serve_ip, serve_port))


data_dis = np.load("Displacement.npy")  # 读取真实数据
num = 0
tem = 20
strain = 5

# 传输数据
while True:
    num += 1
    time.sleep(5)  # 5s读取间隔
    send_data = []

    # 真实数据 + 模拟范围 + 高斯噪声
    send_data.append(time.asctime())  # 获取当前时间
    send_data.append(data_dis[num * 20, 0])
    send_data.append(random.choice((-1, 1)) + tem + random.gauss(0, 0.5))
    send_data.append(random.choice((-2, -1, 1, 2)) + strain + random.gauss(0, 0.5))
    send_data.append(random.choice((-3, -2, -1, 0, 1, 2, 3)) + random.gauss(0, 0.5))

    tem = send_data[1]
    strain = send_data[2]
    dic = {}
    dic['data'] = send_data
    dicJson = json.dumps(dic)

    tcp_socket.send(dicJson.encode("gbk"))  # Json编码传递

    if send_data == "break":
        break

    from_server_msg = tcp_socket.recv(1024)  # 接受1024字节信息
    print(from_server_msg.decode("gbk"))  # 解码输出

# 关闭连接
tcp_socket.close()
