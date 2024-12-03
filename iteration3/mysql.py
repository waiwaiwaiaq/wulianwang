import pymysql


class Mysql(object):
    def __init__(self):
        try:
            self.conn = pymysql.connect(host='localhost', user='root', password='123456', database='Sensor', port=3306)
            self.cursor = self.conn.cursor()  # 用来获得python执行Mysql命令的方法（游标操作）
            print("连接数据库成功")
        except:
            print("连接失败")

    def getItems(self):
        sql = "SELECT * FROM Bridge"    #获取food数据表的内容
        self.cursor.execute(sql)
        items = self.cursor.fetchall()  #接收全部的返回结果行
        return items
