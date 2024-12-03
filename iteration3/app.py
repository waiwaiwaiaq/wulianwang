from flask import Flask, render_template
from data import SourceData
import pymysql

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='123456',
    db='Sensor',
)

app = Flask(__name__)

# http://127.0.0.1:8081/api/datastream
@app.route('/api/datastream')
def index():
    data = SourceData()
    return render_template('index.html', form=data, title=data.title)


# http://127.0.0.1:8081
@app.route('/')
def hello_world():
    cur = conn.cursor()
    sql = "select * from Bridge"
    cur.execute(sql)
    content = cur.fetchall()
    data_ = []
    for i in range(len(content)):
        data__ = []
        print(content[i])
        for j in range(len(content[i])):
            if j == 0 or j == 1:
                data__.append(content[i][j])
            else:
                data__.append(round(float(content[i][j]), 2))
        data_.append(data__)
    labels = ["时间", "序号", "位移", "温度", "应变", "GPS"]
    return render_template('table.html', labels=labels, content=data_)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8081, debug=True)
