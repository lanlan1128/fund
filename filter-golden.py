## 策略
# 1.五四三二法则,近一年排名1/5,近两年排名1/4,近三年排名1/3,近五年排名1/2
# 2.规模适中（20至100亿）
# 3.只有一位基金经理
# 3.基金经理工作年限较久（从事证券相关工作和直接管理基金的两个角度；最好工作时间大于3年）


import pandas as pd
import numpy as np
import time

fileName = 'rawDATA-golden-{}'.format(time.strftime("%Y-%m-%d", time.localtime()))
f = open('./{}.csv'.format(fileName))
data = pd.read_csv(f)

data.近3年增幅 = data.近3年增幅.replace('--', np.nan)
data = data.dropna(axis=0,how='any')
data.近5年增幅 = data.近5年增幅.replace('---', np.nan)
data = data.dropna(axis=0,how='any')

# 基金规模筛选
data.基金规模 = data.基金规模.str.extract('(\d+\.?\d*)', expand=False)
data['基金规模'] = data['基金规模'].apply(pd.to_numeric, errors='coerce')
data = data[data.apply(lambda x : 20 < x.基金规模 < 100, axis=1)]

# 5432法则
data.近1年排名 = data.近1年排名.replace('--', np.nan)
data = data.dropna(axis=0,how='any')
data.近2年排名 = data.近2年排名.replace('--', np.nan)
data = data.dropna(axis=0,how='any')
data.近3年排名 = data.近3年排名.replace('--', np.nan)
data = data.dropna(axis=0,how='any')
data.近5年排名 = data.近5年排名.replace('---', np.nan)
data = data.dropna(axis=0,how='any')

rateRule = [1/2, 1/3, 1/4, 1/5]
for idx, i in enumerate(['近1年排名', '近2年排名', '近3年排名', '近5年排名']):
    data[i + '系数'] = data[i].str.split('|').map(lambda x: int(x[0])/int(x[1]))
    data = data[data[i+'系数'] < rateRule[idx]]

# 筛选只有一个基金经理的
data = data.loc[~(data['基金经理'].str.contains('等'))]

data.to_csv('./{}{}.csv'.format(fileName, '-筛选后版本'))