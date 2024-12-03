import pymysql

# 连接mysql
database = pymysql.connect(user='root',password='123456',host='localhost',port=3306, database='Sensor')

# 查看连接状态
cursor = database.cursor()

sql_1 = "CREATE DATABASE IF NOT EXISTS Sensor"
cursor.execute(sql_1)

sql='''
        create table Bridge(
        time varchar(100),
        no varchar(100),
        data1 varchar(100),
        data2 varchar(100),
        data3 varchar(100),
        data4 varchar(100)
        )
    '''
cursor.execute(sql)

cursor.close()
database.close()
