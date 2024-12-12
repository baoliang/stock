#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import talib as tl

__author__ = 'bob '
__date__ = '2024/12/8'


## 超越中轨
# 第一个指标：日线向上突破布林线中轨和五日线（同时突破最好）
# 第二个指标：成交量交上一日放大1.5倍以上
# 第三个指标：主力净流入-净占比占比10%以上（也可以稍稍放宽）
# 第四个指标：没有连续涨停
# 第五个指标： 换手率大于五
# 第六个指标：收盘价高于开盘价
# 第五个指标： CCI 81天＞100  
# SELECT * FROM (SELECT sss.DATE,sss.CODE, 
# sss.NAME,sss.new_price,
# sss.deal_amount,sss.pre_close_price,cn_stock_indicators.boll,
# cn_stock_fund_flow.fund_rate,cn_stock_indicators.boll_ub,
# (SELECT ss.deal_amount FROM cn_stock_spot AS ss WHERE ss.date=  DATE_SUB(sss.date,  INTERVAL 1 DAY) AND ss.code =sss.code) AS pre_amount
#  FROM cn_stock_spot AS sss
#  LEFT JOIN cn_stock_indicators ON sss.date= cn_stock_indicators.date AND sss.code = cn_stock_indicators.code
#   LEFT JOIN cn_stock_fund_flow ON sss.date= cn_stock_fund_flow.date AND sss.code = cn_stock_fund_flow.code
#     LEFT JOIN cn_stock_selection ON sss.date= cn_stock_selection.date AND sss.code = cn_stock_selection.code
#   WHERE cn_stock_fund_flow.fund_rate  > 10 AND sss.new_price > sss.pre_close_price  
#   AND  sss.new_price     BETWEEN  LEAST(cn_stock_indicators.boll_lb, cn_stock_indicators.boll_ub) * 0.8 AND LEAST(cn_stock_indicators.boll_lb, cn_stock_indicators.boll_ub) * 1.2
#   AND  sss.new_price >  cn_stock_indicators.boll AND sss.DATE ='2024-12-10'
#   AND cn_stock_selection.turnoverrate > 5
  
#   ) AS beyond WHERE beyond.deal_amount > beyond.pre_amount*1.5 

#    LIMIT 3000 
def check(code_name, data, date=None, threshold=30):
    if date is None:
        end_date = code_name[0]
    else:
        end_date = date.strftime("%Y-%m-%d") 
    if end_date is not None:
        mask = (data['date'] <= end_date)
        data = data.loc[mask].copy()
    if len(data.index) < threshold:
        return False

    data.loc[:, 'ma30'] = tl.MA(data['close'].values, timeperiod=30)
    data['ma30'].values[np.isnan(data['ma30'].values)] = 0.0

    data = data.tail(n=threshold)

    step1 = round(threshold / 3)
    step2 = round(threshold * 2 / 3)

    if data.iloc[0]['ma30'] < data.iloc[step1]['ma30'] < \
            data.iloc[step2]['ma30'] < data.iloc[-1]['ma30'] and data.iloc[-1]['ma30'] > 1.2 * data.iloc[0]['ma30']:
        return True
    else:
        return False
