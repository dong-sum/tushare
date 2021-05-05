import requests

headers = {"User-Agent":"hui bo tou zi fen xi/2.5.5 (iPhone; iOS 14.4; Scale/2.00)",
           "Cookie":"safedog-flow-item=B51B3C6B0CC13D2D20E9766C4E571EB8",
           "Accept-Language":"zh-Hans-CN;q=1, en-CN;q=0.9, zh-Hant-CN;q=0.8, el-CN;q=0.7",
           "Content-Length":"52", "Accept-Encoding":"gzip, deflate", "Connection":"keep-alive"}
datas = {"action":"sign", "btype": "22", "systype": "iOS", "username": "iWhU5XlWiU"}
r = requests.post("http://mp.hibor.com.cn/MobilePhone/GetJsonHandler.ashx", data=datas, headers=headers)
#返回的文本信息
print(r.text)
#接口返回状态码
print(r.status_code)
#解析文本
