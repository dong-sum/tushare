import tushare as ts
from datetime import datetime
import datetime
import time
import os
import traceback
import utils

#增加判断是否止损的策略，每日下午5点执行

IN_CODE = os.environ['IN_CODE']  //从环境变量中获取要判断的代码 用&分割
code_value = IN_CODE.split('&')


TOKEN = os.environ['TS_TOKEN']
ts.set_token(TOKEN)
pro = ts.pro_api()

#是否止损
def cutLoss():
  end_date = utils.getTradeCal(1)
  for code in code_value:
    code = code.replace('\n', '')
    first = code[0]
    if first == '0' or first == '3':
      code = code + '.SZ'
    elif first == '6':
      code = code + '.SH'

    df = ts.pro_bar(ts_code=code, adj='qfq', start_date="20190101", end_date=end_date,
                    ma=[5, 10, 20, 30, 60, 120, 250])
    
    execute(code, df, 'ma250')
    execute(code, df, 'ma120')
    execute(code, df, 'ma60')
    execute(code, df, 'ma30')

    
def execute(df, ma):
  pre_ma_value = df.loc[1, ['ma250']]
    ma_value = df.loc[0, ['ma250']]
    #收盘价
    pre_close_value = df.loc[1, ['close']]
    close_value = df.loc[0, ['close']]
    if close_value < ma_value and pre_close_value < pre_ma_value:
      print('如果止损线为' + ma + '，那么该卖了')
    
    
cutLoss()   
    