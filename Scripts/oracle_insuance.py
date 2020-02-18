# 区块链中写一个模块，可以发送没有区块链中非内置函数的数据
# 预言机负责收集这些数据，并且负责验证这些数据，验证完毕后返回给区块链
# 由于预言机的内容是随师可被编辑的，所以可以在其中加入任意模板变量函数
# FLASK接收接口，接收数据并处理，并生成对应的哈希文件和类型名
# FLASK返回数据，区块链把ttype加入self.ttype中，子树根哈希值直接返回到root根哈希值，实验验证可以验证内/外部数据
import hashlib
import json
from argparse import ArgumentParser

from flask import Flask, jsonify
from flask import request

def hash_1(data):
    json_string = json.dumps(data,sort_keys=True).encode()
    # print('//hash 1: %s' % hashlib.sha256(json_string).hexdigest())
    return hashlib.sha256(json_string).hexdigest()

def hash_2(data1, data2):
    data = '%s%s' % (data1, data2)
    json_string = json.dumps(data, sort_keys=True).encode()
    # print('//hash 2: %s' % hashlib.sha256(json_string).hexdigest())
    return hashlib.sha256(json_string).hexdigest()

def make_leaf_root(insurance):
    # 填补空白二叉位置
    if len(insurance) % 2 == 1:
        insurance.append('ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff')
    while len(insurance) > 1:
        # 动态填补空白二叉位置
        if len(insurance) % 2 == 1:
            insurance.append('ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff')
        length = len(insurance)
        # print('1')
        # print(len(insurance))
        i = 0
        j = 1
        n = 0
        # print(insurance[i])
        # print(insurance[j])
        # list中元素两两hash
        print('temp hash is %s' % insurance)
        # 子树哈希值记录
        f = open('insurance.txt','a')
        f.write(str(insurance) + '\n')
        f.close()
        while i != length:
            # print('2')
            t = hash_2(insurance[i], insurance[j])
            # print('temp hash i is %s ,temp hash j is %s' % (insurance[i],insurance[j]))
            # print(t)
            insurance[n] = t
            i = i + 2
            j = j + 2
            n = n + 1
        # list分片
        insurance = insurance[0:length // 2]
    return insurance[0]

insurance_record = []
def speed_record(ttype,car_driver,speed):
    global insurance_record
    insurance_record.append(
        {
            'T-Type': ttype,
            'Car_driver':car_driver,
            'Speed':speed
    }
    )





oracle = Flask(__name__)

@oracle.route('/confirm_data',methods = ['POST'])
def confirm_data():
    values = request.get_json()
    checktype = values['T-Type']
    if checktype == 'insurance':
        check = ['T-Type', 'Car_driver', 'Speed']
        # 检查数据完整性
        if values is None:
            return 'Error:No Data input', 400
        if not all(k in check for k in values):
            return 'Missing Data input', 400
        speed_record(values['T-Type'], values['Car_driver'], values['Speed'])
        print('oracle message receive')
    else:
        return 'Wrong T-Type', 400
    return 'message has been received',201

@oracle.route('/backdata',methods = ['GET'])
def back_data():
    global insurance_record
    f = open('insuarance.txt','w')
    f.close()
    i = 0
    for temp_record in insurance_record:
        insurance_record[i] = hash_1(temp_record)
        i = i + 1
    insurance = make_leaf_root(insurance_record)
    # 这里就默认预言机和区块链都部署在本地，避免网络延时对实验数据带来的影响
    insurance_record = []
    return jsonify([insurance]),200

if __name__=='__main__':
    parser=ArgumentParser()
    parser.add_argument('-p', '--port', default=8000, help='input your using port')
    args=parser.parse_args()
    port=args.port
    oracle.run(host='0.0.0.0', port=port, debug=True)