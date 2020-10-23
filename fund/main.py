# -*- coding: utf-8 -*-
"""
 @Topic:主调用函数
 @Date:
 @Author: terry.wang
"""
import logging
from lib_fund import libFund
import csv

# 不传则会从 json中读取，更推荐配置json的方式
fund_code_list = ['512000', '270002']  # ,'161219','110035','001210','008488','001938','002621']

ff = libFund(level=logging.INFO)
# 获取基金列表的实时涨跌幅
ff.fund_current_jjjz()
# 获取基金列表的持有收益率
ff.fund_rate_estimate()
# 获取基金列表的持有总金额和持有收益金额,实时估算收益
ff.fund_hold_amount_income()
# 获取单个基金的历史几天的 单位净值 历史净值 日收益率
his_jjjz=ff.fund_history_jjjz('161219', 2)
# # 获取单个基金的股票持仓情况及股票实时的涨跌幅
hold_shares2=ff.fund_hold_shares('161219')

# with open("tmp.csv",'w',encoding='utf-8-sig') as f:
#     writer = csv.writer(f,dialect='excel')
#     writer.writerow(['净值日期','单位净值','累计净值','日增长率'])
#     for row in his_jjjz:
#         writer.writerow(row)
#         # writer.writerows(row)


