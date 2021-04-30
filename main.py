import utils
from datetime import datetime
import _thread
import os
import threading

QZ_VALUE_1 = os.environ['QZ_VALUE_1']
qz_value = QZ_VALUE_1.split('&')

writeM250Path = './result/{}/filter{}-M250.txt'
writeM120Path = './result/{}/filter{}-M120.txt'
writeM60Path = './result/{}/filter{}-M60.txt'
writeM30Path = './result/{}/filter{}-M30.txt'

date = str(datetime.now().date()).replace('-', '')
isExists = os.path.exists('./result/' + date)
if not isExists:
    os.makedirs('./result/' + date)

def writeM250():
    try:
        print("M250筛选，文件写入执行开始")
        date = str(datetime.now().date()).replace('-', '')
        writePath = writeM250Path.replace('{}', date)
        count = 0
        end_date = utils.getTradeCal(1)
        result = ''
 
        count = 0
        for line in qz_value:
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
        print('-------------输出结果开始------------------')
        print(result)
        print('-------------输出结果结束------------------')
        
        f1 = open(writePath, 'w')

        f1.write(result)
        f1.close()

        print("M250筛选，文件写入执行结束")
    except Exception as e:
        print(traceback.format_exc())
        logging.error('错误，原因为: ' + str(e))

def writeM120():
    print("M120筛选，文件写入执行开始")
    date = str(datetime.now().date()).replace('-', '')
    writePath = writeM120Path.replace('{}', date)
    # isExists = os.path.exists(writePath)
    # if not isExists:
    #     os.makedirs(writePath)
    count = 0
    end_date = utils.getTradeCal(1)
    # result = end_date + '\n'
    result = ''

    count = 0
    for line in qz_value:
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
    print('-------------输出结果开始------------------')
    print(result)
    print('-------------输出结果结束------------------')

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
    count = 0
    end_date = utils.getTradeCal(1)
    result = ''

    count = 0
    for line in qz_value:
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
    print('-------------输出结果开始------------------')
    print(result)
    print('-------------输出结果结束------------------')

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
    count = 0
    end_date = utils.getTradeCal(1)
    result = ''

    count = 0
    for line in qz_value:
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
    print('-------------输出结果开始------------------')
    print(result)
    print('-------------输出结果结束------------------')

    f1 = open(writePath, 'w')

    f1.write(result)
    f1.close()

    print("M30筛选，文件写入执行结束")

#####################################

#writeM250()
#writeM120()
#writeM60()
#writeM30()


threads = []
threads.append(threading.Trhead(target=writeM250))
threads.append(threading.Trhead(target=writeM120))
threads.append(threading.Trhead(target=writeM60))
threads.append(threading.Trhead(target=writeM30))

for t in threads:
    print(t)
    t.start()

