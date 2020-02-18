import json


import requests
from flask import Flask, jsonify

headers = {'content-type': 'application/json'}
rsuurl = 'http://127.0.0.1:5000/transactions/new'  # 修改，以及模板数据
data_json = {
    "T-Type": "dsrc",
    "Sender": "b",
    "Receiver": "a",
    "M-Type": "res",
    "Msg": "1faw4fadadc",
    "Communication object": "v2v"
}
for i in range(1,5):
    res = requests.post(url=rsuurl, data=json.dumps(data_json), headers=headers)

data_json = {
    "T-Type":"fees",
    "Sender":"a",
    "Receiver":"b",
    "M-Type":"res",
    "Msg":"5a8c0f7e",
    "Fees":10
}

for i in range(1,5):
    res = requests.post(url=rsuurl, data=json.dumps(data_json), headers=headers)

data_json = {
    "T-Type":"trafficvio",
    "Sender":"a",
    "Receiver":"b",
    "License plate":"苏A.12345"
}

for i in range(1,5):
    res = requests.post(url=rsuurl, data=json.dumps(data_json), headers=headers)

data_json = {
    'R-Type': "speed",
    'Car_driver': "苏A.12345",
    'Speed': "121"
}

for i in range(1,5):
    res = requests.post(url=rsuurl, data=json.dumps(data_json), headers=headers)
rsuurl = 'http://127.0.0.1:5000/mine'
res = requests.get(url=rsuurl)