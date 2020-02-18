import json
import hashlib
import requests
from time import time
from numpy import *

from flask import Flask, jsonify

def hash_2(data1, data2):
    data = '%s%s' % (data1, data2)
    json_string = json.dumps(data, sort_keys=True).encode()
    # print('//hash 2: %s' % hashlib.sha256(json_string).hexdigest())
    return hashlib.sha256(json_string).hexdigest()

def countSpvTime1():
    headers = {'content-type': 'application/json'}
    rsuurl = 'http://127.0.0.1:5000/transaction/check1'  # 修改，以及模板数据

    startTimeStamp1 = time()
    # post把要验证的交易发送给服务器端，服务器端接收到后把该数据到根的匹配数据存储到list中，返回到light node中，lightnode使用hash2计算值并进行对比
    data_json_check = {
        "T-Type": "dsrc",
        "Sender": "a",
        "Receiver": "b",
        "M-Type": "res",
        "Msg": "c928b4d3f",
        "Communication object": "v2v"
    }

    res = requests.post(url=rsuurl, data=json.dumps(data_json_check), headers=headers)
    res_dict = json.loads(res.text)
    corelist = res_dict['core_list']
    neighbourlist = res_dict['neighbour_list']
    print(corelist)
    print(neighbourlist)

    i = 0
    j = 0
    check_flag = True
    core_length = len(corelist)
    print(core_length)
    # 循环验证树上数据
    while True:
        # 结束判断条件
        if i + 1 == core_length:
            break
        core_check_data = corelist[i]
        neighbour_check_data = neighbourlist[j]
        next_check_core_data = corelist[i + 1]
        # print('coredata is:',core_check_data)
        # print('neighbour data is:',neighbour_check_data)
        # print('next data is:',next_check_core_data)

        if hash_2(core_check_data, neighbour_check_data) == next_check_core_data or hash_2(neighbour_check_data,
                                                                                           core_check_data) == next_check_core_data:
            print(core_check_data, neighbour_check_data)
            print('equal')
        else:
            print(core_check_data, neighbour_check_data)
            print(hash_2(core_check_data, neighbour_check_data), hash_2(neighbour_check_data, core_check_data))
            print('not equal')
            check_flag = False
            break
        i = i + 1
        j = j + 1
    if check_flag == True:
        print('check pass,correct transaction')
    else:
        print('this data is fake')

    endTimeStamp1 = time()
    time1 = endTimeStamp1 - startTimeStamp1
    print('time use is:', time1)
    return time1

def countSpvTime2():
    headers = {'content-type': 'application/json'}
    rsuurl = 'http://127.0.0.1:5000/transaction/check2'  # 修改，以及模板数据

    startTimeStamp2 = time()
    # post把要验证的交易发送给服务器端，服务器端接收到后把该数据到根的匹配数据存储到list中，返回到light node中，lightnode使用hash2计算值并进行对比
    data_json_check = {
        "T-Type": "trafficvio",
        "Sender": "b",
        "Receiver": "a",
        "License plate": "苏A.54321"
    }

    res = requests.post(url=rsuurl, data=json.dumps(data_json_check), headers=headers)
    res_dict = json.loads(res.text)
    corelist = res_dict['core_list']
    neighbourlist = res_dict['neighbour_list']
    print(corelist)
    print(neighbourlist)

    i = 0
    j = 0
    check_flag = True
    core_length = len(corelist)
    print(core_length)
    # 循环验证树上数据
    while True:
        # 结束判断条件
        if i + 1 == core_length:
            break
        core_check_data = corelist[i]
        neighbour_check_data = neighbourlist[j]
        next_check_core_data = corelist[i + 1]
        # print('coredata is:',core_check_data)
        # print('neighbour data is:',neighbour_check_data)
        # print('next data is:',next_check_core_data)

        if hash_2(core_check_data, neighbour_check_data) == next_check_core_data or hash_2(neighbour_check_data,
                                                                                           core_check_data) == next_check_core_data:
            print(core_check_data, neighbour_check_data)
            print('equal')
        else:
            print(core_check_data, neighbour_check_data)
            print(hash_2(core_check_data, neighbour_check_data), hash_2(neighbour_check_data, core_check_data))
            print('not equal')
            check_flag = False
            break
        i = i + 1
        j = j + 1
    if check_flag == True:
        print('check pass,correct transaction')
    else:
        print('this data is fake')

    endTimeStamp2 = time()
    time2 = endTimeStamp2 - startTimeStamp2
    print('time use is:', time2)
    return time2

def countSpvTime3():
    headers = {'content-type': 'application/json'}
    rsuurl = 'http://127.0.0.1:5000/transaction/check3'  # 修改，以及模板数据

    startTimeStamp3 = time()
    # post把要验证的交易发送给服务器端，服务器端接收到后把该数据到根的匹配数据存储到list中，返回到light node中，lightnode使用hash2计算值并进行对比
    data_json_check = {
        "T-Type": "fees",
        "Sender": "a",
        "Receiver": "b",
        "M-Type": "res",
        "Msg": "0f7dca23f5a8c",
        "Fees": 20
    }

    res = requests.post(url=rsuurl, data=json.dumps(data_json_check), headers=headers)
    res_dict = json.loads(res.text)
    corelist = res_dict['core_list']
    neighbourlist = res_dict['neighbour_list']
    print(corelist)
    print(neighbourlist)

    i = 0
    j = 0
    check_flag = True
    core_length = len(corelist)
    print(core_length)
    # 循环验证树上数据
    while True:
        # 结束判断条件
        if i + 1 == core_length:
            break
        core_check_data = corelist[i]
        neighbour_check_data = neighbourlist[j]
        next_check_core_data = corelist[i + 1]
        # print('coredata is:',core_check_data)
        # print('neighbour data is:',neighbour_check_data)
        # print('next data is:',next_check_core_data)

        if hash_2(core_check_data, neighbour_check_data) == next_check_core_data or hash_2(neighbour_check_data,
                                                                                           core_check_data) == next_check_core_data:
            print(core_check_data, neighbour_check_data)
            print('equal')
        else:
            print(core_check_data, neighbour_check_data)
            print(hash_2(core_check_data, neighbour_check_data), hash_2(neighbour_check_data, core_check_data))
            print('not equal')
            check_flag = False
            break
        i = i + 1
        j = j + 1
    if check_flag == True:
        print('check pass,correct transaction')
    else:
        print('this data is fake')

    endTimeStamp3 = time()
    time3 = endTimeStamp3 - startTimeStamp3
    print('time use is:', time3)
    return time3

spv1 = []
spv2 = []
spv3 = []
for i in range(10):
    temp1 = countSpvTime1()
    temp2 = countSpvTime2()
    temp3 = countSpvTime3()
    spv1.append(temp1)
    spv2.append(temp2)
    spv3.append(temp3)
    print(spv1)
    print(spv2)
    print(spv3)

print('spv1 mean is:',mean(spv1))
print('spv2 mean is:', mean(spv2))
print('spv3 mean is:', mean(spv3))
spvmean = (mean(spv1) + mean(spv2) + mean(spv3)) / 3
print('avg spv is:',spvmean)
#----------------------------------------------------------------------------------


# print('time1 use is:',time1)
# print('time2 use is:',time2)
# print('The ave time is',(time1 + time2) / 2)

# # 从full_node获取链上的交易数据
# res = requests.get(url=rsuurl)
# res_dict = json.loads(res.text)
#
# print(res_dict['chain'][0])