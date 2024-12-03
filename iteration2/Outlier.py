import pandas as pd


class WMA(object):
    @staticmethod
    def get_wma_weights(span, flag=True):
        paras = range(1, span + 1)
        count = sum(paras)
        if flag:
            return [float(para) / count for para in paras]
        else:
            return [float(para) / count for para in paras][::-1]

    def get_wma_values(self, datas):

        wma_values = []
        wma_keys = datas.index
        for length in range(1, len(datas) + 1):
            wma_value = 0
            weights = self.get_wma_weights(length)
            for index, weight in zip(datas.index, weights):
                wma_value += datas[index] * weight
            wma_values.append(wma_value)
        return pd.Series(wma_values, wma_keys)


def calculate_variance(dps, moving_average):
    variance = 0
    count = 0
    for index in range(len(dps)):
        variance += (dps.to_numpy()[index] - moving_average.to_numpy()[index]) ** 2
    variance /= (len(dps) - count)
    return variance


f = open('gps.txt', encoding='gbk')
txt = []
for line in f:
    txt.append(float(line.strip()))


data_dict_series = {}
for i in range(len(txt)):
    data_dict_series[str(i)] = txt[i]

dps = pd.Series(data_dict_series)

wma_line = WMA().get_wma_values(dps)

# 计算标准差
wma_var = calculate_variance(dps, wma_line)

for index in wma_line.index:
    if not (wma_line[index] - wma_var <= dps[index] <= wma_line[index] + wma_var):
        print("异常点", dps[index])
