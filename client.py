#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: supeihuang
# Time: 2019/5/10 16:30
#模拟postman进行测试
import requests
import json
url='http://127.0.0.1:5000/transactions/new'
headers = {'content-type': 'application/json'}
data_json= {
	"T-Type":"dsrc",
	"Sender":"a",
	"Receiver":"b",
	"M-Type":"res",
	"Msg":"5a8c0f7e",
	"Communication object":"v2v"
}

res =requests.post(url=url, data=json.dumps(data_json),headers = headers)
simWords = res.json()
print(simWords)