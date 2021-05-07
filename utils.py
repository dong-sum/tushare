import tushare as ts
from datetime import datetime
import datetime
import time
import os
import traceback

def init():
    global dict
    TOKEN = os.environ['TS_TOKEN']
    ts.set_token(TOKEN)
    global pro
    pro = ts.pro_api()
    return pro

#获取成交量
#入参：日期  出参：成交量（单位：手 float类型）
def getVol(ts_code, trade_date):
    # pro = ts.pro_api()
    df = pro.daily(ts_code=ts_code, trade_date=trade_date)
    # '002007.SZ'
    # '20201211'
    # vol = df[['vol']]
    vol = df.iat[0, 9]
    if vol > 0:

        # print(ts_code + " 在 " + trade_date + " 的成交量：" + str(vol))
        return vol
    else:
        # print("没数据")
        return 0
    # print(df)

# 获取股东人数
def getHolderNum(ts_code, enddate):
    df = pro.stk_holdernumber(ts_code=ts_code, end_date=enddate)
    if df is not None:
        return df.loc[0, ['holder_num']][0]

# 获取均线和均量
# 通用行情接口
def getBar():
    # a = ts.pro_bar(ts_code='000001.SZ', adj='qfq', start_date='20180101', end_date='20181011')
    # print(a)
    df = ts.pro_bar(ts_code="002007.SZ", adj='qfq', start_date="20190101", end_date="20201211",
                    ma=[5, 10, 20, 30, 60, 120, 250])
    ma5 = df.loc[0, ['ma5']]
    ma10 = df.loc[0, ['ma10']]
    ma20 = df.loc[0, ['ma20']]
    ma30 = df.loc[0, ['ma30']]
    ma60 = df.loc[0, ['ma60']]
    ma120 = df.loc[0, ['ma120']]
    # 250均线数据不准, 排查下复权是否需要设置
    ma250 = df.loc[0, ['ma250']]

    print(ma5)
    print(ma10)
    print(ma20)
    print(ma30)
    print(ma60)
    print(ma120)
    print(ma250)
    # print(df)

# 获取交易日历
# num:返回几条交易日的信息
def getTradeCal(num):
    now = datetime.datetime.now()
    formatNow = now.strftime("%Y%m%d")
        # .strftime("%Y%m%d")
    delte = datetime.timedelta(days=180)
    n_date = now - delte
    formateDate = n_date.strftime("%Y%m%d")
    # print(formatNow)
    # print(formateDate)
    df = pro.trade_cal(exchange="", start_date=formateDate, end_date=formatNow, is_open="1")
    tempdf = df.tail(num)

    # 日历列
    # tempDf = df[['cal_date']]
    vol = 0
    #ts_code = "002007.SZ"
    #for index, row in tempdf.iterrows():
     #   vol = vol + getVol(ts_code, row.cal_date)
        # print(row.cal_date)

   # vol = vol / 50
    # print(ts_code + " 在50日均成交量：" + str(vol))

    if(len(tempdf) == 0):
        return tempdf.cal_date

    # for row in tempdf:
    #     print(i["cal_date"])
    # df.
    # print(df)

def getM120(ts_code, end_date, ma):
    # ts_code = "002007.SZ"
    if ts_code not in dict:
        df = ts.pro_bar(ts_code=ts_code, adj='qfq', start_date="20190101", end_date=end_date,
                    ma=[5, 10, 20, 30, 60, 120, 250])
        dict[ts_code] = df
    # print(ts_code)
    if df is None:
        return
    count = 0
    status = False
    try:
        ma250_value = df.loc[0, ['ma250']]
        ma120_value = df.loc[0, ['ma120']]
        ma60_value = df.loc[0, ['ma60']]
        now_value = df.loc[0, ['high']]

        #筛选-剔除年线下方的，60日均线法剔除120日线下方的，30日均线法剔除60日和120日线下方的-start
        if now_value[0] < ma250_value[0]:
            return
        if ma == 'ma60' and now_value[0] < ma120_value[0]:
            return
        if ma == 'ma30' and (now_value[0] < ma120_value[0] or now_value[0] < ma60_value[0]):
            return
        #筛选-end

        #筛选-剔除连续4天5日线下跌-start
        value_0 = df.loc[0, ['ma5']][0]
        value_1 = df.loc[1, ['ma5']][0]
        value_2 = df.loc[2, ['ma5']][0]
        value_3 = df.loc[3, ['ma5']][0]
        value_4 = df.loc[4, ['ma5']][0]
        if value_0 < value_1 and value_1 < value_2 and value_2 < value_3 and value_3 < value_4:
            return
        #筛选-剔除连续4天5日线下跌-end

        for index, row in df.iterrows():
            count = count+1
            # if count == 1:
            #     continue
            if count > 15:
                break
            # print(ts_code)
            #120日均线
            pre_ma_value = df.loc[index+1, [ma]]
            ma_value = df.loc[index, [ma]]
            #收盘价
            pre_close_value = df.loc[index+1, ['close']]
            close_value = df.loc[index, ['close']]
            #最高价
            pre_high_value = df.loc[index + 1, ['high']]
            high_value = df.loc[index, ['high']]
            #最低价
            pre_low_value = df.loc[index + 1, ['low']]
            low_value = df.loc[index, ['low']]
            #涨跌幅
            pct_chg = df.loc[index, ['pct_chg']]

            #收盘价站上ma日均线
            if close_value[0] >= ma_value[0] and pre_close_value[0] <= pre_ma_value[0]:
                status = True
                # print(getName(ts_code) + ts_code + "站上120线的日期" + df.loc[index, ['trade_date']][0])
            elif close_value[0] <= ma_value[0] and pre_close_value[0] >= pre_ma_value[0]:
                a = 1
                # status = True
                # print(getName(ts_code) + ts_code +  "跌破120日均线的日期" + row.trade_date)

            if high_value[0] >= ma_value[0] and pre_high_value[0] <= pre_ma_value[0]:
                status = True
                # print(getName(ts_code) + ts_code + "最高点站上120日均线" + row.trade_date)
            elif low_value[0] <= ma_value[0] and pre_low_value[0] >= pre_ma_value[0]:
                a = 1
                # status = True
                # print(getName(ts_code) + ts_code + "最低点跌破120日均线" + row.trade_date)
                # print("（可观察是否是回踩120日均线的情况）")
    except:
        print("报错：" + ts_code)
    if status:
        # print("-----------------" + getName(ts_code) + ts_code + " end-------------------------")
        # return getName(ts_code) + ts_code
        return ts_code

def getM250(ts_code, end_date, ma):
    if ts_code not in dict:
        df = ts.pro_bar(ts_code=ts_code, adj='qfq', start_date="20190101", end_date=end_date,
                    ma=[5, 10, 20, 30, 60, 120, 250])
        dict[ts_code] = df
    # print(ts_code)
    if df is None:
        return
    count = 0
    status = False
    try:
        ma250_value = df.loc[0, ['ma250']]
        ma120_value = df.loc[0, ['ma120']]
        ma60_value = df.loc[0, ['ma60']]
        now_value = df.loc[0, ['high']]

        #筛选-剔除年线下方的，60日均线法剔除120日线下方的，30日均线法剔除60日和120日线下方的-start
        if now_value[0] < ma250_value[0]:
            return
        if ma == 'ma60' and now_value[0] < ma120_value[0]:
            return
        if ma == 'ma30' and (now_value[0] < ma120_value[0] or now_value[0] < ma60_value[0]):
            return
        #筛选-end

        #筛选-剔除连续4天5日线下跌-start
        value_0 = df.loc[0, ['ma5']][0]
        value_1 = df.loc[1, ['ma5']][0]
        value_2 = df.loc[2, ['ma5']][0]
        value_3 = df.loc[3, ['ma5']][0]
        value_4 = df.loc[4, ['ma5']][0]
        if value_0 < value_1 and value_1 < value_2 and value_2 < value_3 and value_3 < value_4:
            return
        #筛选-剔除连续4天5日线下跌-end

        for index, row in df.iterrows():
            count = count+1
            # if count == 1:
            #     continue
            if count > 15:
                break
            # print(ts_code)
            #250日均线
            pre_ma_value = df.loc[index+1, [ma]]
            ma_value = df.loc[index, [ma]]
            #收盘价
            pre_close_value = df.loc[index+1, ['close']]
            close_value = df.loc[index, ['close']]
            #最高价
            pre_high_value = df.loc[index + 1, ['high']]
            high_value = df.loc[index, ['high']]
            #最低价
            pre_low_value = df.loc[index + 1, ['low']]
            low_value = df.loc[index, ['low']]
            #涨跌幅
            pct_chg = df.loc[index, ['pct_chg']]

            #收盘价站上ma日均线
            if close_value[0] >= ma_value[0] and pre_close_value[0] <= pre_ma_value[0]:
                status = True
                # print(getName(ts_code) + ts_code + "站上250线的日期" + df.loc[index, ['trade_date']][0])
            elif close_value[0] <= ma_value[0] and pre_close_value[0] >= pre_ma_value[0]:
                a = 1
                # status = True
                # print(getName(ts_code) + ts_code +  "跌破250日均线的日期" + row.trade_date)

            if high_value[0] >= ma_value[0] and pre_high_value[0] <= pre_ma_value[0]:
                status = True
                # print(getName(ts_code) + ts_code + "最高点站上250日均线" + row.trade_date)
            elif low_value[0] <= ma_value[0] and pre_low_value[0] >= pre_ma_value[0]:
                a = 1
                # status = True
                # print(getName(ts_code) + ts_code + "最低点跌破250日均线" + row.trade_date)
                # print("（可观察是否是回踩250日均线的情况）")
    except:
        print("报错：" + ts_code)
    if status:
        return ts_code

def getName(ts_code):
    df = pro.stock_basic(ts_code=ts_code)
    name = df.loc[0, ['name']]
    return name[0]

def getHKHold(ts_code):
    #一分钟只能调用两次
    df = pro.hk_hold(ts_code=ts_code, trade_date='20201218')
    #持股量
    vol = df.loc[0, ['vol']]
    #持股比例
    ratio = df.loc[0, ['ratio']]
    print("aa")

init()

#获取涨停跌停价
def getLimit(end_date):
    data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    result = ''
    for index, row in data.iterrows():
        ts_code = data.loc[index, ['ts_code']][0]
        if ts_code[0 : 3] == '688':
            continue
        # if
        # 一分钟只能获取60次,每20秒执行一次
        time.sleep(20)
        df = ts.pro_bar(ts_code=ts_code, adj='qfq', start_date="20190101", end_date=end_date)

        if df is None:
            return
        count = 0

        #涨停数量
        up_limit_count = 0
        try:
            for index, row in df.iterrows():
                count = count + 1
                trade_date = df.loc[index, 'trade_date']

                df_limit = pro.stk_limit(ts_code=ts_code, trade_date=trade_date)
                if df_limit is None:
                    return

                if count > 20:
                    break
                value = df.loc[index, 'close']
                up_limit = df_limit.loc[0, 'up_limit']
                if value == up_limit:
                    up_limit_count = up_limit_count + 1

            if up_limit_count > 1:
                result = result + ts_code[0:6] + '\n'
                print("临时输出" + result)
        except Exception as e:
            print(e)
            print("报错：" + ts_code)

    return result

#获取20个交易日内有两次超过9%的股票
def getUp(date):
    data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    result = ''
    try:
        for index, row in data.iterrows():
            ts_code = data.loc[index, 'ts_code']
            if ts_code[0: 3] == '688':
                continue
            # date = str(datetime.now().date()).replace('-', '')
            df = ts.pro_bar(ts_code=ts_code, adj='qfq', start_date="20190101", end_date=date)

            if df is None:
                continue
            count = 0
            num = 0
            for index, row in df.iterrows():
                num = num + 1
                if num > 20:
                    break
                pct_chg = df.loc[index, 'pct_chg']
                print("执行中：" + ts_code + ":" + str(pct_chg) + "%")
                if pct_chg > 9.8:
                    print("涨幅：" + str(pct_chg))
                    count = count + 1
                    if count > 1:
                        result = result + ts_code[0:6] + '\n'
                        break
    except Exception as e:
        print(e)
        print("报错：" + ts_code)
    return result
