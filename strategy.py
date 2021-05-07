import tushare as ts
from datetime import datetime
import datetime
import time
import os
import traceback
import utils
import mailUtils

#增加判断是否止损的策略，每日下午5点执行

IN_CODE = os.environ['IN_CODE']  #从环境变量中获取要判断的代码 用&分割
code_value = IN_CODE.split('&')

IN_CODE_2 = os.environ['IN_CODE_2']
if IN_CODE_2 is not None:
  code_value.append(IN_CODE_2)


TOKEN = os.environ['TS_TOKEN']
ts.set_token(TOKEN)
pro = ts.pro_api()

#是否止损
def cutLoss():
  end_date = utils.getTradeCal(1)
  global res
  res = ''
  for code in code_value:
    code = code.replace('\n', '')
    first = code[0]
    if first == '0' or first == '3':
      code = code + '.SZ'
    elif first == '6':
      code = code + '.SH'

    print('------------------start----------------------')
    data = pro.stock_basic(ts_code=code)
    print(data.loc[0, ['name']][0])
      
    df = ts.pro_bar(ts_code=code, adj='qfq', start_date="20190101", end_date=end_date,
                    ma=[5, 10, 20, 30, 60, 120, 250])
    res = res + '\n' + '------------------start----------------------'
    res = res + '\n' + data.loc[0, ['name']][0]
    res = res + '\n' + execute(code, df, 'ma250')
    res = res + '\n' + execute(code, df, 'ma120')
    res = res + '\n' + execute(code, df, 'ma60')
    res = res + '\n' + execute(code, df, 'ma30')
    res = res + '\n' + '-------------------end-----------------------'
    print('-------------------end-----------------------')
   # mailUtils.sendText('是否止损', res)

    
def execute(code, df, ma):
  pre_ma_value = df.loc[1, [ma]][0]
  ma_value = df.loc[0, [ma]][0]
  #收盘价
  pre_close_value = df.loc[1, ['close']][0]
  close_value = df.loc[0, ['close']][0]
 
  if close_value < ma_value and pre_close_value < pre_ma_value:
    print(code + '如果止损线为' + ma + '，那么果断该卖了')
    return '如果止损线为' + ma + '，那么果断该卖了'
  else:
    print(code + '如果止损线为' + ma + '，那么再捂一捂哦，别着急卖')
    return '如果止损线为' + ma + '，那么再捂一捂哦，别着急卖'
    
    
cutLoss()  
mailUtils.sendText('是否止损', res)


    
