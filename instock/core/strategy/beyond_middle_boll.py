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
# 第五个指标： CCI 81天＞100  
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
