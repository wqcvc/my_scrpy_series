# -*- coding: utf-8 -*-
"""
 @Topic:主调用函数
 @Date:
 @Author: terry.wang
"""
import logging
from lib_fund import libFund

ff = libFund(level=logging.INFO)

# 获取基金列表的实时涨跌幅,持有总金额,持有收益金额,实时估算收益,持有收益率
funds_total = ff.fund_hold_info
title2 = ['基金名称', '基金代码', '实时涨跌幅', '当日收益估算', '持有收益率', '总收益', '持有总金额']
csv_name2 = "持仓实时数据和收益明细.csv"
# ff.csv_save(funds_total, title=title2, csv_name=csv_name2)

# 获取单个基金的股票持仓情况及股票实时的涨跌幅
csv_name1 = '基金前十持仓股票明细.csv'
quote_list = ['161219']  # #ff.fund_list
for i in range(len(quote_list)):
    res = ff.fund_hold_shares(quote_list[i])
    title1 = [f"{ff.code_to_name(quote_list[i])}({quote_list[i]})"]
    # ff.csv_save(res, title1, csv_name1)

# 获取单个基金的历史几天的 单位净值 历史净值 日收益率
his_jjjz_list = ['161219']
days = 30
his_jjjz = ff.fund_history_jjjz(his_jjjz_list[0], days)
title3 = ['净值日期', '单位净值', '累计净值', '日增长率']
csv_name3 = f"{ff.code_to_name(his_jjjz_list[0])}({his_jjjz_list[0]})近{days}天净值.csv"
# ff.csv_save(his_jjjz, title=title3, csv_name=csv_name3)
