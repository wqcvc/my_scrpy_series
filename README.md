python爬虫系列：

####一.91porn视频下载:
  ```介绍：91porn网站的视频爬虫+破解下载视频 最新版本根据 cdn编号下载
  功能列表：
    1.按请求个数爬取并自动下载: start_by_number(number=2)
    2.按请求页数爬取并自动下载: start_by_page(page=1)
    3.按照url单个下载：start_by_url(url)
```


####二.基金爬虫fund
```
  介绍：针对天天基金的各种基金信息的爬虫
  功能列表：
    1.获取基金列表的实时涨跌幅
      ff.fund_current_jjjz()
    2.获取基金列表的持有收益率
      ff.fund_rate_estimate()
    3.获取基金列表的持有总金额 + 持有收益金额 + 实时估算收益
      ff.fund_hold_info
    4.单个基金股票前10数据 + 仓位占比重
      ff.fund_hold_shares('163406')
    5.单个基金的历史单位净值 + 历史净值 + 日收益率
      ff.fund_history_jjjz('512000', 1)
    6.全部基金列表: 基金名字 基金代码 类型
      all_list = ff.funds_all_list(to_file=0)
    7.历史各种涨幅数据 : 共31项 1-阶段涨幅(10项) 2-季度涨幅(8个季度) 3-年度涨幅(8年) 4-持有人结构(最近一期的5项数据)
      sss1 = ff.fund_his_rates(['270002','161219'])
    8.基础信息 : 规模变动信息（8个季度） + 基金经理任期管理信息（5项数据）
      sss2 = ff.fund_basic_info(['270002','161219'])
    9.基金特色数据: 标准差 + 夏普率。
      sss3 = ff.fund_special_info(['000002'])
    10.基金汇总保存进同一个csv + xlsx. 可以不连续请求。eg: 0:2 2:5 5:10分段 
    (重要：次函数存在性能问题。需要使用此功能请关注同目录下的 pypter_aysn.py 使用了协程异步请求，极大提高了请求效率)
      ff.funds_full_info([0, 6945])
    11.存储进mysql
      to do
    12.定期更新数据库内容
      to do
    13.to be continue...
```
  
####三.myflask
  ```
  规划中
  ```

