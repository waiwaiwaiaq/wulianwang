from socket import *
import pymysql
import json

# 连接mysql
database = pymysql.connect(user='root', password='123456', host='localhost', port=3306, database='Sensor')
# 查看连接状态(true,false)
cursor = database.cursor()
sql = 'truncate table Bridge'
cursor.execute(sql)

# 创建TCP连接
tcp_server = socket(AF_INET, SOCK_STREAM)

# 连接端口
address = ('100.78.82.242', 8081)
tcp_server.bind(address)
tcp_server.listen(128)  # 用户数目

# 接收对方发送过来的数据
client_socket, clientAddr = tcp_server.accept()
print("连接成功")

num_ = 0
while True:
    from_client_msg = client_socket.recv(1024)  # 接收1024字节
    print("接收的数据：", from_client_msg.decode("gbk"))  # 解码
    num_ += 1
    data = from_client_msg.decode("gbk")

    data = json.loads(data)

    info_list = [data['data'][0], str(num_), data['data'][1], data['data'][2], data['data'][3], data['data'][4]]
    sql = "insert into Bridge values(%s, %s, %s, %s, %s, %s)"

    # 列表传参
    cursor.execute(sql, info_list)
    database.commit()

    send_data = client_socket.send("已收到信息".encode("gbk"))  # 回复

# 关闭
client_socket.close()
cursor.close()
database.close()
