# 单模板-最坏时间复杂度
# 本实验将录入各种数据各1000个，并把目标实验数据postman中的dsrc放在最后一个

import json
import requests


n = 3000
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
for i in range(1,n):
    res = requests.post(url=rsuurl, data=json.dumps(data_json), headers=headers)
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

# data_json = {
#     'R-Type': "speed",
#     'Car_driver': "苏A.12345",
#     'Speed': "120"
# }
#
# for i in range(1,2):
#     res = requests.post(url=rsuurl, data=json.dumps(data_json), headers=headers)

rsuurl = 'http://127.0.0.1:5000/mine'
res = requests.get(url=rsuurl)