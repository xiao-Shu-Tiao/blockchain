import hashlib
import json

# 首先定义区块链模板
import uuid
from argparse import ArgumentParser
from time import time, sleep
from urllib.parse import urlparse

import requests
from flask import Flask, jsonify
from flask import request

car = Flask(__name__)

@car.route('/carengine', methods=['POST'])
def carmsg():
    originmsg = 'i need to stop' # 修改
    # car1 to car2
    msg = {
        'message':originmsg
    }
    headers = {'content-type': 'application/json'}
    # car1 to car2
    car2url = 'http:car2' # 修改
    requests.post(url=car2url, data=json.dumps(msg), headers=headers)

    # car1 to rsu
    rsuurl = 'http:rsu' # 修改，以及模板数据
    data_json = {
        "T-Type": "dsrc",
        "Sender": "b",
        "Receiver": "a",
        "M-Type": "res",
        "Msg": originmsg,
        "Communication object": "v2v"
    }
    res = requests.post(url=rsuurl, data=json.dumps(data_json), headers=headers)
    simWords = res.json()
    print(simWords)
    response = 'engine start'
    return jsonify(response),201

@car.route('/carmsg', methods=['POST'])
def carmsg():
    msg = 'message ack'
    response = msg
    return jsonify(response),201

if __name__=='__main__':
    # 输入port入口
    # 启动项
    parser=ArgumentParser()
    # 设定运行格式python xxx.py -p/-port,help提示在python xxx.py -h 会出现
    parser.add_argument('-p', '--port', default=80, help='input your using port')
    # 解析输入的参数
    args=parser.parse_args()
    # args.xxx   xxx由设定参数-port确定
    port=args.port

    car.run(host='0.0.0.0', port=port, debug=True)