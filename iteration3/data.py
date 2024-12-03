from mysql import Mysql


class SourceDataDemo:

    def __init__(self):
        # 标题
        self.title = '基坑监测管理平台'

        # 文字展示
        self.counter = {'name': '监测长度', 'value': 164.31}
        self.counter2 = {'name': '预警个数', 'value': 5}

        self.db = Mysql()
        self.items = self.db.getItems()
        self.data1 = {}
        self.data2 = {}
        self.data3 = {}
        self.data4 = {}

        for i in range(len(self.items)):
            self.data1[self.items[i][1]] = float(self.items[i][2])
            self.data2[self.items[i][1]] = float(self.items[i][3])
            self.data3[self.items[i][1]] = float(self.items[i][4])
            self.data4[self.items[i][1]] = float(self.items[i][5])

        print(self.data1)
        self.echart1_data = {
            'title': '位移传感器数据',
            'data': []
        }
        for i in range(len(self.items)):
            self.echart1_data['data'].append((i, self.data1[self.items[i][1]]))

        self.echart2_data = {
            'title': '温度传感器数据',
            'data': []
        }
        for i in range(len(self.items)):
            self.echart2_data['data'].append((i, self.data2[self.items[i][1]]))

        self.echart4_data = {
            'title': '应变数据',
            'data': [],
        }
        for i in range(len(self.items)):
            self.echart4_data['data'].append((i, self.data3[self.items[i][1]]))

        self.echart5_data = {
            'title': 'GPS数据',
            'data': []
        }
        for i in range(len(self.items)):
            self.echart5_data['data'].append((i, self.data4[self.items[i][1]]))


    @property
    def echart1(self):
        data = self.echart1_data
        echart = {
            'title': data.get('title'),
            # 第一次get获取到的是许多键值对，所以需要对每个键值对再次get
            'xAxis': [],
            'series': []
        }
        for i in range(len(data['data'])):
            echart['xAxis'].append(data['data'][i][0])
            echart['series'].append(data['data'][i][1])
        # 返回的是标题和对应的数据，并没有说用什么方式展现！
        return echart

    @property
    def echart2(self):
        data = self.echart2_data
        echart = {
            'title': data.get('title'),
            'xAxis': [],
            'series': []
        }
        for i in range(len(data['data'])):
            echart['xAxis'].append(data['data'][i][0])
            echart['series'].append(data['data'][i][1])
        return echart

    @property
    def echart4(self):
        data = self.echart4_data
        echart = {
            'title': data.get('title'),
            'xAxis': [],
            'series': [],
        }
        for i in range(len(data['data'])):
            echart['xAxis'].append(data['data'][i][0])
            echart['series'].append(data['data'][i][1])
        return echart

    @property
    def echart5(self):
        data = self.echart5_data
        echart = {
            'title': data.get('title'),
            'xAxis': [],
            'series': [],
        }
        for i in range(len(data['data'])):
            echart['xAxis'].append(data['data'][i][0])
            echart['series'].append(data['data'][i][1])
        return echart

    @property
    def echart6(self):
        data = self.echart6_data
        echart = {
            'title': data.get('title'),
            'xAxis': [i.get("name") for i in data.get('data')],
            'data': data.get('data'),
        }
        return echart

    @property
    def map_1(self):
        data = self.map_1_data
        echart = {
            'symbolSize': data.get('symbolSize'),
            'data': data.get('data'),
        }
        return echart


class SourceData(SourceDataDemo):

    def __init__(self):
        """
        按照 SourceDataDemo 的格式覆盖数据即可
        """
        super().__init__()
        self.title = '桥梁无线监测综合管理平台'
