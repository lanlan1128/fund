import requests
import demjson
import datetime
import time
from pandas.core.frame import DataFrame
from bs4 import BeautifulSoup
# import json
import re
import pandas as pd
from multiprocessing import Pool
import logging




def rank_data_crawl(time_interval='3n', ft='all'):
    fund_list = []
    fund_names = [
      '华安逆向策略混合',
      '易方达蓝筹精选混合',
      '景顺长城新兴成长混合'
    ]

    for fund_name in fund_names:
        search_url = 'http://fundsuggest.eastmoney.com/FundSearch/api/FundSearchAPI.ashx?m=1&key=%s' % fund_name 
        fund_rq = requests.get(search_url)
        fund_text = fund_rq.text
        fund_rawdata = demjson.decode(fund_text)
        for i in fund_rawdata['Datas']:
            fund_list.append(i['CODE'].split(','))

    return fund_list

# 详情页面的抓取
def get_allFund_content(single_fund_urls):
    try:
        single_fund_url = single_fund_urls[0]
        rang_fund_url = single_fund_urls[1]
        
        # print(single_fund_url)
        # if infromation[3] !='理财型' and infromation[3] !='货币型' and infromation[2].endswith('(后端)')==False:
        #     code = infromation[0]
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
        r = requests.get(single_fund_url, headers=headers)
        r.encoding = r.apparent_encoding #避免中文乱码
        soup = BeautifulSoup(r.text, 'html.parser')
        
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
        rang = requests.get(rang_fund_url, headers=headers)
        rang.encoding = rang.apparent_encoding #避免中文乱码
        soupRang = BeautifulSoup(rang.text, 'html.parser')

        # # 判断交易状态
        # staticItem = soup.select('.staticItem')[0].get_text()
        # if '终止' in staticItem or '认购' in staticItem:
        #     pass
        # else:
            # 各项指标
            # 基金名、基金类型、单位净值、累计净值、基金规模、成立日、评级、基金涨幅及排名
            # （近1周、近1月、近3月、近6月、今年来、近1年、近2年、近3年、近5年、基金经理）
        fund_code = single_fund_url[26:32]
        # fund_name = re.match('[\u4e00-\u9fffA-Za-z]+', soup.select('.fundDetail-tit > div')[0].get_text()).group()        
        fund_name = soup.select('.SitePath > a')[2].get_text()
        unit_netValue = soup.select('.dataItem02 > .dataNums > span.ui-font-large')[0].get_text()
        accumulative_netValue = soup.select('.dataItem03 > .dataNums > span.ui-font-large')[0].get_text()
        fund_info = [i for i in soup.select('div.infoOfFund tr > td')]
        # fund_type1 = fund_info[0].get_text().split('：')[1].strip()
        fund_type = re.search('：[DQI\-\u4e00-\u9fffA]+', fund_info[0].get_text()).group()[1:]
        fund_scale = fund_info[1].get_text().split('：')[1].strip()
        fund_manage = fund_info[2].get_text().split('：')[1].strip()
        fund_establishmentDate = fund_info[3].get_text().split('：')[1].strip()
        # fund_grade = fund_info[5].get_text().split('：')[1].strip()
        fund_Rdata = soup.select('#increaseAmount_stage > .ui-table-hover div.Rdata ')#指数基金多一排，考虑re或者排名倒着写
        func_Rate = soupRang.select('.jdzfnew > ul > li')
        
        fund_1weekAmount = fund_Rdata[0].get_text()
        fund_1monthAmount = fund_Rdata[1].get_text()
        fund_3monthAmount = fund_Rdata[2].get_text()
        fund_6monthAmount = fund_Rdata[3].get_text()
        fund_thisYearAmount = fund_Rdata[4].get_text()
        fund_1yearAmount = fund_Rdata[5].get_text()
        fund_2yearAmount = fund_Rdata[6].get_text()
        fund_3yearAmount = fund_Rdata[7].get_text()
        fund_1weekRank = fund_Rdata[-8].get_text()
        fund_1monthRank = fund_Rdata[-7].get_text()
        fund_3monthRank = fund_Rdata[-6].get_text()
        fund_6monthRank = fund_Rdata[-5].get_text()
        fund_thisYearRank = fund_Rdata[-4].get_text()
        fund_1yearRank = fund_Rdata[-3].get_text()
        fund_2yearRank = fund_Rdata[-2].get_text()
        fund_3yearRank = fund_Rdata[-1].get_text()
        fund_5yearRank = func_Rate[(10 * 7 - 3)].get_text()
        fund_5yearAmount = func_Rate[(10 * 7 - 6)].get_text()
        fund_allyearAmount = func_Rate[11 * 7 - 6].get_text()
        fund_1yearRank_rate = rate(fund_1yearRank)
        fund_2yearRank_rate = rate(fund_2yearRank)
        fund_3yearRank_rate = rate(fund_3yearRank)
        fund_5yearRank_rate = rate(fund_5yearRank)

        Fund_data = [fund_code, fund_name, fund_type, unit_netValue, accumulative_netValue,
                     fund_scale, fund_establishmentDate,
                     fund_1weekAmount, fund_1monthAmount, fund_3monthAmount,fund_6monthAmount,
                     fund_thisYearAmount, fund_1yearAmount, fund_2yearAmount, fund_3yearAmount, fund_5yearAmount, fund_allyearAmount,
                     fund_1weekRank, fund_1monthRank, fund_3monthRank, fund_6monthRank, fund_thisYearRank,
                     fund_1yearRank, fund_2yearRank, fund_3yearRank, fund_5yearRank, fund_manage, fund_1yearRank_rate, fund_2yearRank_rate, fund_3yearRank_rate, fund_5yearRank_rate]
        
        return Fund_data
    except Exception as e:
        # print('Error:', single_fund_url, str(e))
        logging.exception('Error:', single_fund_url, str(e))


def rate(str):
    try:
        fund_1yearRank_rate = (lambda x: int(x[0]) / int(x[1]))(str.split('|'))
    except: 
        fund_1yearRank_rate = 0

    return f'{round(fund_1yearRank_rate * 100, 2)}%'

def main():
    #  初始化区域
    main1_name = ['基金代码']
    main2_name = ['基金代码', '基金简称', '基金类型', '单位净值', '累计净值', '基金规模', '成立日期',\
                  '近1周增幅', '近1月增幅', '近3月增幅', '近6月增幅', '今年来增幅', '近1年增幅', '近2年增幅', '近3年增幅', '近5年增幅', '成立以来涨幅',\
                  '近1周排名', '近1月排名', '近3月排名', '近6月排名', '今年来排名', '近1年排名', '近2年排名', '近3年排名', '近5年排名', '基金经理', '近1年排名百分比(%)', '近2年排名百分比(%)', '近3年排名百分比(%)', '近5年排名百分比(%)']
    # ########################## 先爬API接口 ###################################
    rawData = rank_data_crawl()
    
    # 数据清洗
    rawData = DataFrame(rawData, columns=main1_name)

    # ########################## 单页面抓取 ###################################
    # 获取抓取的detail网址
    detail_urls_list = [['http://fund.eastmoney.com/{}.html'.format(i) , 'http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jdzf&code={}'.format(i)] for i in rawData['基金代码']]
    print('#详情页面的抓取#启动时间：', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    middle = datetime.datetime.now()
    # 多线程
    p = Pool(4)
    all_fund_data = p.map(get_allFund_content, detail_urls_list)
    p.close()
    p.join()
    while None in all_fund_data:
        all_fund_data.remove(None)
    end = datetime.datetime.now()
    print('#详情页面的抓取#用时：', str(end - middle))
    print('程序结束时间：', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    all_fund_data = DataFrame(all_fund_data, columns=main2_name)

    # 表合并
    data_merge = pd.merge(rawData, all_fund_data, how='left', on='基金代码')
    
    # 文件储存
    file_content = pd.DataFrame(data=data_merge)
    file_content.to_csv('./rawDATA-golden-{}.csv'.format(time.strftime("%Y-%m-%d", time.localtime())), encoding='gbk')


if __name__ == '__main__':
    main()
