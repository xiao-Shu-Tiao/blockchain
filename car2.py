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

@car.route('/carmsg', methods=['POST'])
def carmsg():
    originmsg = 'ok'#修改
    response = {
        'message':originmsg
    }

    # msg to rsu
    rsuurl = 'http://127.0.0.1:5000/transactions/new'# 修改
    headers = {'content-type': 'application/json'}
    data_json = {
        "T-Type": "dsrc",
        "Sender": "b",
        "Receiver": "a",
        "M-Type": "ack",
        "Msg": originmsg,
        "Communication object": "v2v"
    }
    res = requests.post(url=rsuurl, data=json.dumps(data_json), headers=headers)
    simWords = res.json()
    print(simWords)

    return jsonify(response),201

if __name__=='__main__':
    # 输入port入口
    # 启动项
    parser=ArgumentParser()
    # 设定运行格式python xxx.py -p/-port,help提示在python xxx.py -h 会出现
    parser.add_argument('-p', '--port', default=800, help='input your using port')
    # 解析输入的参数
    args=parser.parse_args()
    # args.xxx   xxx由设定参数-port确定
    port=args.port

    car.run(host='0.0.0.0', port=port, debug=True)