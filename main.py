import utils
from datetime import datetime
import _thread
import os

#截取第一位到第6位的字符  str[0,6]
# print('001002.SZ'[0:6])

#筛选近20 交易日出现突破120日线的标的
#2020-12-26增加规则：股价在250日线上方
path = './resource/data.txt'
writeM250Path = './result/{}/filter{}-M250.txt'
writeM120Path = './result/{}/filter{}-M120.txt'
writeM60Path = './result/{}/filter{}-M60.txt'
writeM30Path = './result/{}/filter{}-M30.txt'
# sortPath = './resource/sort.txt'

date = str(datetime.now().date()).replace('-', '')
isExists = os.path.exists('./result/' + date)
if not isExists:
    os.makedirs('./result/' + date)

def writeM250():
    print("M250筛选，文件写入执行开始")
    date = str(datetime.now().date()).replace('-', '')
    writePath = writeM250Path.replace('{}', date)
    f = open(path, mode='r', encoding='utf-8')
    count = 0
    end_date = utils.getTradeCal(1)
    result = ''

    count = 0
    for line in f.readlines():
        line = line.replace('\n', '')
        first = line[0]
        if first == '0' or first == '3':
            line = line + '.SZ'
        elif first == '6':
            line = line + '.SH'
        res = utils.getM250(line, end_date, 'ma250')
        if res is not None and res[0 : 3] != '688':

            count = count + 1
            temp = res[0 : 6]
            result = result + temp + '\n'

    print("ma250个数：" + str(count))

    f1 = open(writePath, 'w')

    f1.write(result)
    f1.close()

    print("M250筛选，文件写入执行结束")

def writeM120():
    print("M120筛选，文件写入执行开始")
    date = str(datetime.now().date()).replace('-', '')
    writePath = writeM120Path.replace('{}', date)
    # isExists = os.path.exists(writePath)
    # if not isExists:
    #     os.makedirs(writePath)
    f = open(path, mode='r', encoding='utf-8')
    count = 0
    end_date = utils.getTradeCal(1)
    # result = end_date + '\n'
    result = ''

    count = 0
    for line in f.readlines():
        line = line.replace('\n', '')
        first = line[0]
        if first == '0' or first == '3':
            line = line + '.SZ'
        elif first == '6':
            line = line + '.SH'
        res = utils.getM120(line, end_date, 'ma120')
        if res is not None and res[0 : 3] != '688':

            count = count + 1
            temp = res[0 : 6]
            result = result + temp + '\n'

    print("ma120个数：" + str(count))

    f1 = open(writePath, 'w')

    f1.write(result)
    f1.close()

    print("M120筛选，文件写入执行结束")

##################################################
def writeM60():
    print("M60筛选，文件写入执行开始")
    date = str(datetime.now().date()).replace('-', '')
    writePath = writeM60Path.replace('{}', date)
    # isExists = os.path.exists(writePath)
    # if not isExists:
    #     os.makedirs(writePath)
    f = open(path, mode='r', encoding='utf-8')
    count = 0
    end_date = utils.getTradeCal(1)
    result = ''

    count = 0
    for line in f.readlines():
        line = line.replace('\n', '')
        first = line[0]
        if first == '0' or first == '3':
            line = line + '.SZ'
        elif first == '6':
            line = line + '.SH'
        res = utils.getM120(line, end_date, 'ma60')
        if res is not None and res[0 : 3] != '688':
            count = count + 1
            # print(res)
            temp = res[0 : 6]
            result = result + temp + '\n'

    print("ma60个数：" + str(count))

    f1 = open(writePath, 'w')

    f1.write(result)
    f1.close()

    print("M60筛选，文件写入执行结束")

##################################################
def writeM30():
    print("M30筛选，文件写入执行开始")
    date = str(datetime.now().date()).replace('-', '')
    writePath = writeM30Path.replace('{}', date)
    # isExists = os.path.exists(writePath)
    # if not isExists:
    #     os.makedirs(writePath)
    f = open(path, mode='r', encoding='utf-8')
    count = 0
    end_date = utils.getTradeCal(1)
    result = ''

    count = 0
    for line in f.readlines():
        line = line.replace('\n', '')
        first = line[0]
        if first == '0' or first == '3':
            line = line + '.SZ'
        elif first == '6':
            line = line + '.SH'
        res = utils.getM120(line, end_date, 'ma30')
        if res is not None and res[0 : 3] != '688':
            count = count + 1
            temp = res[0 : 6]
            result = result + temp + '\n'

    print("ma30个数：" + str(count))

    f1 = open(writePath, 'w')

    f1.write(result)
    f1.close()

    print("M30筛选，文件写入执行结束")


#####################################
#做三个文件的交集-待办
def getSub():
    date = str(datetime.now().date()).replace('-', '')
    writePath_120 = writeM120Path.replace('{}', date)
    writePath_60 = writeM60Path.replace('{}', date)
    writePath_30 = writeM30Path.replace('{}', date)
    writePath = './result/{}/交集-{}.txt'.replace('{}', date)
    # isExists = os.path.exists(writePath)
    # if not isExists:
    #     os.makedirs(writePath)
    f = open(writePath_120, mode='r', encoding='utf-8')

    arr_120 = getArray(writePath_120)
    arr_60 = getArray(writePath_60)
    arr_30 = getArray(writePath_30)

    arr_temp = []
    for value_120 in arr_120:
        for value_60 in arr_60:
            if value_120 == value_60:
                for value_30 in arr_30:
                    if value_60 == value_30:
                        arr_temp.append(value_120)
    print(arr_temp)
    # print(arr_120)
    # print(arr_60)
    # print(arr_30)
    result = ''
    for value in arr_temp:
        result = result + value + '\n'

    f1 = open(writePath, 'w')

    f1.write(result)
    f1.close()

    print("三个文件交集，文件写入执行结束")

def getArray(path):
    arr = []
    f = open(path, mode='r', encoding='utf-8')

    for line in f.readlines():
        line = line.replace('\n', '')
        arr.append(line)
    return arr


#跌破5日线，均线多头，5/10/20/30向上

#涨停数大于1
##################################################
def getLimit():
    print("涨停数大于1，文件写入执行开始")
    date = str(datetime.now().date()).replace('-', '')
    write_path = './resource/涨停个数大于1-{}.txt'.replace('{}', date)
    f = open(path, mode='r', encoding='utf-8')
    result = utils.getLimit(date)

    f1 = open(write_path, 'w')
    f1.write(result)
    f1.close()

    print("涨停数大于1，文件写入执行结束")

def getHoldNum():
    print("获取股东数-开始")
    date = str(datetime.now().date()).replace('-', '')
    open_path = './resource/交集-{}.txt'.replace('{}', date)
    write_path = './resource/交集-含股东数-{}.txt'.replace('{}', date)
    f = open(open_path, mode='r', encoding='utf-8')
    # count = 0
    # end_date = utils.getTradeCal(1)
    result = ''

    count = 0
    for line in f.readlines():
        ts_code = line.replace('\n', '')
        line = line.replace('\n', '')
        first = line[0]
        if first == '0' or first == '3':
            line = line + '.SZ'
        elif first == '6':
            line = line + '.SH'
        res = utils.getHolderNum(line, date)
        result = result + ts_code + ',' + str(res) + '\n'

    f1 = open(write_path, 'w')

    f1.write(result)
    f1.close()
    print("获取股东数-结束")

def getHigh():
    print("获取近20交易日，涨幅大于9%至少两天的股票-开始")
    date = str(datetime.now().date()).replace('-', '')
    write_path = './resource/高涨幅标的-{}.txt'.replace('{}', date)
    result = utils.getUp(date)

    f1 = open(write_path, 'w')
    f1.write(result)
    f1.close()
    print("获取近20交易日，涨幅大于9%至少两天的股票-结束")

writeM250()
writeM120()
writeM60()
writeM30()
# getSub()
# getLimit()
# getHoldNum()

#看是否需要调整精度，比如9.8,9.8
# getHigh()


# try:
   # _thread.start_new_thread(writeM120())
   # _thread.start_new_thread(writeM60())
   # _thread.start_new_thread(writeM30())
   # _thread.start_new_thread(getSub())
   # _thread.start_new_thread(getHigh())
# except:
#    print ("Error: 无法启动线程")

# while 1:
#    pass
