# 多模板-最坏时间复杂度
# 本实验将录入各种数据各1000个，并把目标实验数据postman中的dsrc放在最后一个

import json
import requests

#------------------------------------------------------------------------------------
n = 3000
token50 = int(n * 0.5)
token60 = int(n * 0.6)
token70 = int(n * 0.7)
token80 = int(n * 0.8)
token90 = int(n * 0.9)
templateTypeNum = 2

eachTtypeCount = (n - token90) // templateTypeNum

headers = {'content-type': 'application/json'}
rsuurl = 'http://127.0.0.1:5000/transactions/new'  # 修改，以及模板数据

#1.1------------------------------------------------------------------------------------
data_json = {
    "T-Type":"fees",
    "Sender":"a",
    "Receiver":"b",
    "M-Type":"res",
    "Msg":"5a8c0f7e",
    "Fees":10
}

for i in range(1,eachTtypeCount // 2):
    res = requests.post(url=rsuurl, data=json.dumps(data_json), headers=headers)
#------------------------------------------------------------------------------------

#1.2------------------------------------------------------------------------------------
data_json = {
    "T-Type":"fees",
    "Sender":"a",
    "Receiver":"b",
    "M-Type":"res",
    "Msg":"0f7dca23f5a8c",
    "Fees":20
}

res = requests.post(url=rsuurl, data=json.dumps(data_json), headers=headers)
#------------------------------------------------------------------------------------

#1.3------------------------------------------------------------------------------------
data_json = {
    "T-Type":"fees",
    "Sender":"a",
    "Receiver":"b",
    "M-Type":"res",
    "Msg":"5a8c0f7e",
    "Fees":10
}

for i in range(1,eachTtypeCount // 2):
    res = requests.post(url=rsuurl, data=json.dumps(data_json), headers=headers)
#------------------------------------------------------------------------------------

#2.1------------------------------------------------------------------------------------
data_json = {
    "T-Type":"trafficvio",
    "Sender":"a",
    "Receiver":"b",
    "License plate":"苏A.12345"
}

for i in range(1,eachTtypeCount // 2):
    res = requests.post(url=rsuurl, data=json.dumps(data_json), headers=headers)
#------------------------------------------------------------------------------------

#2.2------------------------------------------------------------------------------------
data_json = {
    "T-Type":"trafficvio",
    "Sender":"b",
    "Receiver":"a",
    "License plate":"苏A.54321"
}

res = requests.post(url=rsuurl, data=json.dumps(data_json), headers=headers)
#------------------------------------------------------------------------------------

#2.3------------------------------------------------------------------------------------
data_json = {
    "T-Type":"trafficvio",
    "Sender":"a",
    "Receiver":"b",
    "License plate":"苏A.12345"
}

for i in range(1,eachTtypeCount // 2):
    res = requests.post(url=rsuurl, data=json.dumps(data_json), headers=headers)
#------------------------------------------------------------------------------------

#3.1------------------------------------------------------------------------------------
data_json = {
    "T-Type": "dsrc",
    "Sender": "b",
    "Receiver": "a",
    "M-Type": "res",
    "Msg": "1faw4fadadc",
    "Communication object": "v2v"
}
for i in range(1,token90):
    res = requests.post(url=rsuurl, data=json.dumps(data_json), headers=headers)
#------------------------------------------------------------------------------------

#check-----------------------------------------------------------------------------------
# 需要查找的数据
check_json = {
	"T-Type": "dsrc",
    "Sender": "a",
    "Receiver": "b",
    "M-Type": "res",
    "Msg": "c928b4d3f",
    "Communication object": "v2v"
}
res = requests.post(url=rsuurl, data=json.dumps(check_json), headers=headers)
#------------------------------------------------------------------------------------

#3.2------------------------------------------------------------------------------------
data_json = {
    "T-Type": "dsrc",
    "Sender": "b",
    "Receiver": "a",
    "M-Type": "res",
    "Msg": "1faw4fadadc",
    "Communication object": "v2v"
}
for i in range(1,token90):
    res = requests.post(url=rsuurl, data=json.dumps(data_json), headers=headers)
#------------------------------------------------------------------------------------


rsuurl = 'http://127.0.0.1:5000/mine'
res = requests.get(url=rsuurl)
