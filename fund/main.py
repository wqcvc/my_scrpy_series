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
#获取基金列表的实时涨跌幅
gszzl=ff.fund_current_jjjz()
#获取基金列表的持有收益率
ff.fund_rate_estimate()
# 获取基金列表的持有总金额 , 持有收益金额,实时估算收益
gssy=ff.fund_hold_amount_income
# 获取单个基金的历史几天的 单位净值 历史净值 日收益率
his_jjjz=ff.fund_history_jjjz('161219', 5)
# # 获取单个基金的股票持仓情况及股票实时的涨跌幅
hold_shares2=ff.fund_hold_shares('163406')

#持仓
title1=['序号','代码','名称','股价','涨跌幅','占比','万股数','市值']
csv_name1="163406_持仓前十.csv"
ff.csv_save(hold_shares2,title=title1,csv_name=csv_name1)

#收益估算
title2=['基金名称','基金代码','当日估算','总收益','持有总金额']
csv_name2="实时收益算计明细.csv"
ff.csv_save(gssy,title=title2,csv_name=csv_name2)

#历史净值
title3=['净值日期','单位净值','累计净值','日增长率']  # 净值日期	单位净值	累计净值	日增长率
csv_name3="161219_历史净值.csv"
ff.csv_save(his_jjjz,title=title3,csv_name=csv_name3)

#实时涨跌幅
title4=['基金名称','基金涨跌幅','估算净值','前日净值'] # 基金名称 基金涨跌幅 估算净值 前日净值
csv_name4="实时涨跌幅.csv"
ff.csv_save(gszzl,title=title4,csv_name=csv_name4)
