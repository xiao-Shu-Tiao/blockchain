# 区块链结构
# {
#     'index':'0-n',
#     'timestamp':time(),
#     'proof':'0x000',
#     'previous_hash':'hex',
#     'transactions':{
#
#     }
#
# }
import hashlib
import json

# 首先定义区块链模板
import os
import uuid
from argparse import ArgumentParser
from time import time, sleep
from urllib.parse import urlparse

import requests
from flask import Flask, jsonify
from flask import request


class Blockchain(object):
    # 初始化参数及创建创世区块,区块链中保存着之前所有链和当前收集到的交易数据
    def __init__(self):
        self.chain=[]
        self.current_transactions=[]
        self.nodes=set()
        self.merkletree=0
        # 创世区块建立
        self.new_block(100,1)
        # t-type初始化
        self.ttype = []

    def register_node(self,node):
        address=urlparse(node)
        self.nodes.add(address.netloc)

    # 验证邻居节点区块是否为真,需要验证previous_hash是否等于前一区块的hash，proof是否满足前n个为0的条件
    def vaild_chain(self,chain):
        n=0
        previous_block=chain[n]
        later_block=chain[n+1]
        # previous_hash=self.last_block['previous_hash']
        # merkle=self.merkle(self.current_transactions)
        while n+1<len(chain):
            if later_block['previous_hash']!=self.hash(previous_block):
                print('hash compare fail')
                return False
            # vaild_proof_of_work(后一区块的proof，后一区块的merkle，当前区块的previous_hash)
            if not self.vaild_proof_of_work(later_block['proof'], later_block['merkle'],later_block['previous_hash']):
                print(later_block['proof'])
                print(later_block['merkle'])
                print(later_block['previous_hash'])
                print('proof compare fail')
                return False
            n+=1
        return True

    def resolve_conflict(self):
        self_length=len(self.chain)
        neighbour=self.nodes
        new_blcok=None

        # 遍历邻居节点
        for node in neighbour:
            # 从邻居节点获取链信息,requests('url')
            url='http://%s/chain'%node
            print(url)
            response= requests.get(url)
            # 接收数据
            if response.status_code==200:
                length=response.json()['length']
                chain=response.json()['chain']
                print('staatus_code is ok')
            # 判断链是否是最长链,不是最长链的话，则被替换
                if self_length<length and self.vaild_chain(chain):
                    self_length=length
                    new_blcok=chain
                    print('compare ok')
        # 如果已经产生了替换
        if new_blcok:
            self.chain=new_blcok
            print('exchange ok')
            return True

        return  False

    # 定义区块的结构体------------------------（区块头+ 区块体）----------------------------
    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'proof': proof,          #0-n的随机数
            'previous_hash': previous_hash or self.hash(self.last_block),
            'transactions': self.current_transactions,
            'merkle':self.merkletree
        }
        # 写进区块
        self.current_transactions = []
        self.chain.append(block)
        return block

    # 收集交易函数----------------------------------（区块体）-------------------------------
    def dsrc(self, ttype, sender, recipient, mtype, hmsg, communtype):
        self.current_transactions.append(
            {
                'T-Type': ttype,
                'Sender': sender,
                'Receiver': recipient,
                'M-Type': mtype,
                'Msg': hmsg,
                'Communication object': communtype
            }
        )
        # 标记该交易所属区块
        return self.last_block['index']+1

    def fees(self, ttype, sender, recipient, mtype, hmsg, fees):
        self.current_transactions.append(
            {
                'T-Type': ttype,
                'Sender': sender,
                'Receiver': recipient,
                'M-Type': mtype,
                'Msg': hmsg,
                'Fees': fees
            }
        )
        # 标记该交易所属区块
        return self.last_block['index']+1

    def traffic_vio(self, ttype, sender, recipient, license_plate):
        self.current_transactions.append(
            {
                'T-Type': ttype,
                'Sender': sender,
                'Receiver': recipient,
                'License plate': license_plate
            }
        )
        # 标记该交易所属区块
        return self.last_block['index']+1


    # 返回最后一个区块
    @property
    def last_block(self):
        return self.chain[-1]

    # sha256运算
    @staticmethod
    def hash(block):
        json_string=json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(json_string).hexdigest()

    # Pow工作量证明,算前n个为0的数组
    def proof_of_work(self):
        proof_randnum=0
        previous_hash=self.hash(self.last_block)
        # 交易信息转字符串
        # current_transactions_string='%s'%(self.current_transactions)
        # current_transactions_string=current_transactions_string.encode()
        # hash(随机数，当前区块交易信息，上一区块哈希值)
        while self.vaild_proof_of_work(proof_randnum,self.merkletree,previous_hash) is False:
            proof_randnum+=1
        return proof_randnum

    # 重复计算符合要求前四位为0的哈希值
    def vaild_proof_of_work(self,proof_randnum,merkle,previous_hash)->bool:
        hash_string='%s%s%s'%(proof_randnum,merkle,previous_hash)
        hash_string=hash_string.encode()
        guess_num=hashlib.sha256(hash_string).hexdigest()
        if guess_num[0:4] == '0000':
            print('block proof:',proof_randnum)
            return True
        else:
            return False

    # def merkle(self,transactions):
    #     json_string = json.dumps(transactions, sort_keys=True).encode()
    #     self.merkletree = hashlib.sha256(json_string).hexdigest()

    # 把不重复的checktype加进来
    def count_ttype_num(self,unsort_type):
        if unsort_type not in self.ttype:
            self.ttype.append(unsort_type)

    # 定义不同ttype的空list，在mine中使用
    def make_ttype_list(self):
        for sort_type in self.ttype:
            exec('self.ttypelist{}= []'.format(sort_type))
            # 制作一个ttype的hash副本，用于存放ttypelist的哈希值
            exec('self.hash_ttypelist{} = []'.format(sort_type))
            # print('make_ttype_list is ok')

    # #  交易写入后再读取ttype
    # def make_ttype_list(self):
    #     temp_list = []
    #     #  把所有不同的T-TYPE类型读取到数组中
    #     for i in self.current_transactions:
    #         ttypeproperty = i.get('T-Type')
    #         if not ttypeproperty in temp_list:
    #             temp_list.append(ttypeproperty)

    # 把current_transactions中属于该ttype的数据全部加入子树
    def arrange_ttype_list(self):
        # print('////self.current_transaction is %s' % self.current_transactions)
        # print('////self.ttype is %s' % self.ttype)
        for sort_tran in self.current_transactions:
            # print('//the sort_tran is %s' % sort_tran)
            for check_ttype in self.ttype:
                # print('the check_ttype value is %s' % check_ttype)
                # print('the sort_tran is %s' % sort_tran['T-Type'])
                # for循环从list拿dict元素
                if check_ttype == sort_tran['T-Type']:
                    # print('//')
                    # 原交易加入self.ttypelist xxxx数组
                    exec('self.ttypelist'+'%s.append(sort_tran)' % check_ttype)
                    # 原交易哈希加入self.hash_ttypelist xxxx中
                    t = self.merkle_hash_1(sort_tran)
                    exec('self.hash_ttypelist' + '%s.append(t)' % check_ttype)
                    # print('the self.ttypelist is %s' % self.ttypelistdsrc)
                    # print('the self.ttypelist is %s' % self.ttypelistfees)

    # def blank_fullfill(self):
    #     for i in self.ttype:
    #         exec('a=len(lenttypelist{})'.format(i))
    #         if count%2 == 1:

    def merkle_hash_1(self,data):
        json_string = json.dumps(data,sort_keys=True).encode()
        # print('//hash 1: %s' % hashlib.sha256(json_string).hexdigest())
        return hashlib.sha256(json_string).hexdigest()

    def merkle_hash_2(self,data1,data2):
        data = '%s%s' % (data1, data2)
        json_string = json.dumps(data,sort_keys=True).encode()
        # print('//hash 2: %s' % hashlib.sha256(json_string).hexdigest())
        return hashlib.sha256(json_string).hexdigest()

    def inside_merkle(self):
        # 统计merkle执行时间
        startTimeStamp = time()
        self.make_ttype_list()
        self.arrange_ttype_list()
        for cur_ttype in self.ttype:
            self.currentttype = cur_ttype
            # self.temp_leaf指向self.ttypelistdsrc等交易的地址
            # print('this is cur_ttype %s' % cur_ttype)
            # print(self.ttypelistdsrc)
            # print(self.ttypelistfees)
            exec('self.temp_leaf = self.ttypelist{}'.format(cur_ttype))
            # 创建动态文件名保存原始交易数据
            exec("self.file = open('{}transaction.txt','w')".format(cur_ttype))
            self.file.write(str(self.temp_leaf) + '\n')
            self.file.close()

            # print('this is self.temp_leaf %s' % self.temp_leaf)
            # self.temp_hash指向self.hash_ttypelist等副本地址
            exec('self.temp_hash = self.hash_ttypelist{}'.format(cur_ttype))
            # print('this is self.temp_hash %s' % self.temp_hash)
            # # 计算叶子节点哈希值
            # for leaf_hash in self.temp_leaf:
            #     temp = self.merkle_hash_1(leaf_hash)
            #     self.temp_hash.append(temp)
            # 计算子树root hash
            self.make_leaf_root()
            # 把temp_hash中最后长度为1的list中的元素添加到子树根list中
            # print('//end temp hash is %s' % self.temp_hash)
            print(cur_ttype)
            if(len(self.temp_hash) == 0):
                break
            print('sub_tree hash is',self.temp_hash)
            self.root_list.append(self.temp_hash[0])
        # 下面要做的是把各个子树的root合称为 merkle root(默认为偶数，填补空白稍后做)
        print(self.root_list)
        self.make_merkle_root()
        self.merkletree = self.root_list[0]
        # 添加merkle root进入root.txt
        self.file = open('root.txt', 'a')
        self.file.write(str(self.root_list) + '\n')
        self.file.close()
        print('merkle tree root is %s' % self.merkletree)
        endTimeStamp = time()
        print('make tree time:',endTimeStamp - startTimeStamp)

    # 计算子树的默克尔根
    def make_leaf_root(self):
        # 填补空白二叉位置
        if len(self.temp_hash) % 2 == 1:
            self.temp_hash.append('ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff')
        while len(self.temp_hash) > 1:
            # 动态填补空白二叉位置
            if len(self.temp_hash) % 2 == 1:
                self.temp_hash.append('ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff')
            length = len(self.temp_hash)
            # print('1')
            # print(len(self.temp_hash))
            i = 0
            j = 1
            n = 0
            # print(self.temp_hash[i])
            # print(self.temp_hash[j])
            # list中元素两两hash
            print('temp hash is %s' % self.temp_hash)
            # 子树哈希值记录
            exec("self.file = open('{}transaction.txt','a')".format(self.currentttype))
            self.file.write(str(self.temp_hash) + '\n')
            self.file.close()
            while i != length:
                # print('2')
                t = self.merkle_hash_2(self.temp_hash[i],self.temp_hash[j])
                # print('temp hash i is %s ,temp hash j is %s' % (self.temp_hash[i],self.temp_hash[j]))
                # print(t)
                self.temp_hash[n] = t
                i = i + 2
                j = j + 2
                n = n + 1
            # list分片
            self.temp_hash = self.temp_hash[0:length//2]

    def make_merkle_root(self):
        # 重置root.txt
        self.file = open('root.txt', 'w')
        self.file.close()
        if len(self.root_list) % 2 == 1:
            self.root_list.append('ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff')
            print('root list is %s' % self.root_list)
        while len(self.root_list) > 1:
            # 动态填补空白二叉位置
            if len(self.root_list) % 2 == 1:
                self.root_list.append('ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff')
            length = len(self.root_list)
            i = 0
            j = 1
            n = 0
            # 各子树根写入root.txt
            self.file = open('root.txt', 'a')
            self.file.write(str(self.root_list) + '\n')
            self.file.close()
            # list中元素两两hash
            while i != length:
                t = self.merkle_hash_2(self.root_list[i],self.root_list[j])
                self.root_list[n] = t
                i = i + 2
                j = j + 2
                n = n + 1
            # list分片
            self.root_list = self.root_list[0:length//2]

    # 导入外部数据,生成默克尔树
    def merkle(self,oracle_data_list):
        self.temp_leaf = []
        self.temp_hash = []
        self.root_list = []
        #将外部预言机跟数据加入到子树根集合中
        for data in oracle_data_list:
            self.root_list.append(data)
            # print('root list is:',self.root_list)
        self.inside_merkle()




    # def dsrc_merkle(self,transactions):
    #     json_string =

def hash_1(data):
    json_string = json.dumps(data,sort_keys=True).encode()
    # print('//hash 1: %s' % hashlib.sha256(json_string).hexdigest())
    return hashlib.sha256(json_string).hexdigest()

def hash_2(data1, data2):
    data = '%s%s' % (data1, data2)
    json_string = json.dumps(data, sort_keys=True).encode()
    # print('//hash 2: %s' % hashlib.sha256(json_string).hexdigest())
    return hashlib.sha256(json_string).hexdigest()

# 这里只以dsrc作为实验数据例子
def readtxt1(check_ttype,light_node_data):
    if check_ttype != 'dsrc':
        print('error input')
        return [],[]
    f = open('dsrctransaction.txt')
    # 记录与每次hash有关的结果值 核心数
    core_hash = []
    # 记录每次需要的邻居哈希值 邻居数
    neighbour_hash = []
    # 临时存储每行存储后的数据
    line_list = []
    # 第一行交易数据空读
    line = f.readline()
    # light_node_data的哈希值
    light_node_hash = hash_1(light_node_data)
    # 读取第一行数据
    line = f.readline()
    i = 0
    line_list.append('')
    for temp in line:
        if temp == '[' or temp == ']' or temp == "'" or temp == " " or temp == "\n":
            continue
        if temp == ',':
            line_list.append('')
            i = i + 1
            continue
        line_list[i] = line_list[i] + str(temp)
    # 验证未被哈希的集合中有没有light_node_data,即第一行的数据是否存在
    flag = False
    count = 0
    line_count = 0
    # 从数组中找light node发来的测试样例,并加入对应哈希值到核心数组中
    for first_line_hash in line_list:
        if first_line_hash == light_node_hash:
            flag = True
            # line_count负责记录每行需要保存的核心数的索引值
            line_count = count
            break
        count = count + 1
    if flag == True:
        print('data has been saving')
    else:
        print('can not find data')
        return [],[]
    # 循环把每一行对应的记录进去,分count奇偶情况
    while line:
        # 数据处理部分
        line_list = []
        i = 0
        line_list.append('')
        for temp in line:
            if temp == '[' or temp == ']' or temp == "'" or temp == " " or temp == "\n":
                continue
            if temp == ',':
                line_list.append('')
                i = i + 1
                continue
            line_list[i] = line_list[i] + str(temp)
        # 索引偶数位置情况
        print(line_list)
        print(line_count)
        if line_count % 2 == 0:
            core_hash.append(line_list[line_count])
            neighbour_hash.append(line_list[line_count + 1])
        else:
            core_hash.append(line_list[line_count])
            neighbour_hash.append(line_list[line_count - 1])
        line = f.readline()
        line_count = line_count // 2
    f.close()
    # 打开root.txt，继续读取
    f = open('root.txt')
    line = f.readline()
    # 在root.txt中找对应子树的line_count
    line_list = []
    i = 0
    line_list.append('')
    for temp in line:
        if temp == '[' or temp == ']' or temp == "'" or temp == " " or temp == "\n":
            continue
        if temp == ',':
            line_list.append('')
            i = i + 1
            continue
        line_list[i] = line_list[i] + str(temp)

    flag = False
    count = 0
    line_count = 0
    for temps in line_list:
        if temps == hash_2(core_hash[-1], neighbour_hash[-1]) or temps == hash_2(neighbour_hash[-1],core_hash[-1]):
            flag = True
            # line_count负责记录每行需要保存的核心数的索引值
            line_count = count
            break
        count = count + 1
    if flag == True:
        print('ROOTdata has been saving')
    else:
        print('can not find data')
        return [], []

    while line:
        line_list = []
        i = 0
        line_list.append('')
        for temp in line:
            if temp == '[' or temp == ']' or temp == "'" or temp == " " or temp == "\n":
                continue
            if temp == ',':
                line_list.append('')
                i = i + 1
                continue
            line_list[i] = line_list[i] + str(temp)
        # 读取到根时候停止
        if len(line_list) == 1:
            core_hash.append(line_list[line_count])
            break
        if line_count % 2 == 0:
            core_hash.append(line_list[line_count])
            neighbour_hash.append(line_list[line_count + 1])
        else:
            core_hash.append(line_list[line_count])
            neighbour_hash.append(line_list[line_count - 1])
        line_count = line_count // 2
        line = f.readline()
    f.close()
    return core_hash,neighbour_hash

def readtxt2(check_ttype,light_node_data):
    if check_ttype != 'trafficvio':
        print('error input')
        return [],[]
    f = open('trafficviotransaction.txt')
    # 记录与每次hash有关的结果值 核心数
    core_hash = []
    # 记录每次需要的邻居哈希值 邻居数
    neighbour_hash = []
    # 临时存储每行存储后的数据
    line_list = []
    # 第一行交易数据空读
    line = f.readline()
    # light_node_data的哈希值
    light_node_hash = hash_1(light_node_data)
    # 读取第一行数据
    line = f.readline()
    i = 0
    line_list.append('')
    for temp in line:
        if temp == '[' or temp == ']' or temp == "'" or temp == " " or temp == "\n":
            continue
        if temp == ',':
            line_list.append('')
            i = i + 1
            continue
        line_list[i] = line_list[i] + str(temp)
    # 验证未被哈希的集合中有没有light_node_data,即第一行的数据是否存在
    flag = False
    count = 0
    line_count = 0
    # 从数组中找light node发来的测试样例,并加入对应哈希值到核心数组中
    for first_line_hash in line_list:
        if first_line_hash == light_node_hash:
            flag = True
            # line_count负责记录每行需要保存的核心数的索引值
            line_count = count
            break
        count = count + 1
    if flag == True:
        print('data has been saving')
    else:
        print('can not find data')
        return [],[]
    # 循环把每一行对应的记录进去,分count奇偶情况
    while line:
        # 数据处理部分
        line_list = []
        i = 0
        line_list.append('')
        for temp in line:
            if temp == '[' or temp == ']' or temp == "'" or temp == " " or temp == "\n":
                continue
            if temp == ',':
                line_list.append('')
                i = i + 1
                continue
            line_list[i] = line_list[i] + str(temp)
        # 索引偶数位置情况
        print(line_list)
        print(line_count)
        if line_count % 2 == 0:
            core_hash.append(line_list[line_count])
            neighbour_hash.append(line_list[line_count + 1])
        else:
            core_hash.append(line_list[line_count])
            neighbour_hash.append(line_list[line_count - 1])
        line = f.readline()
        line_count = line_count // 2
    f.close()
    # 打开root.txt，继续读取
    f = open('root.txt')
    line = f.readline()
    # 在root.txt中找对应子树的line_count
    line_list = []
    i = 0
    line_list.append('')
    for temp in line:
        if temp == '[' or temp == ']' or temp == "'" or temp == " " or temp == "\n":
            continue
        if temp == ',':
            line_list.append('')
            i = i + 1
            continue
        line_list[i] = line_list[i] + str(temp)

    flag = False
    count = 0
    line_count = 0
    for temps in line_list:
        if temps == hash_2(core_hash[-1], neighbour_hash[-1]) or temps == hash_2(neighbour_hash[-1],core_hash[-1]):
            flag = True
            # line_count负责记录每行需要保存的核心数的索引值
            line_count = count
            break
        count = count + 1
    if flag == True:
        print('ROOTdata has been saving')
    else:
        print('can not find data')
        return [], []

    while line:
        line_list = []
        i = 0
        line_list.append('')
        for temp in line:
            if temp == '[' or temp == ']' or temp == "'" or temp == " " or temp == "\n":
                continue
            if temp == ',':
                line_list.append('')
                i = i + 1
                continue
            line_list[i] = line_list[i] + str(temp)
        # 读取到根时候停止
        if len(line_list) == 1:
            core_hash.append(line_list[line_count])
            break
        if line_count % 2 == 0:
            core_hash.append(line_list[line_count])
            neighbour_hash.append(line_list[line_count + 1])
        else:
            core_hash.append(line_list[line_count])
            neighbour_hash.append(line_list[line_count - 1])
        line_count = line_count // 2
        line = f.readline()
    f.close()
    return core_hash,neighbour_hash

def readtxt3(check_ttype,light_node_data):
    if check_ttype != 'fees':
        print('error input')
        return [],[]
    f = open('feestransaction.txt')
    # 记录与每次hash有关的结果值 核心数
    core_hash = []
    # 记录每次需要的邻居哈希值 邻居数
    neighbour_hash = []
    # 临时存储每行存储后的数据
    line_list = []
    # 第一行交易数据空读
    line = f.readline()
    # light_node_data的哈希值
    light_node_hash = hash_1(light_node_data)
    # 读取第一行数据
    line = f.readline()
    i = 0
    line_list.append('')
    for temp in line:
        if temp == '[' or temp == ']' or temp == "'" or temp == " " or temp == "\n":
            continue
        if temp == ',':
            line_list.append('')
            i = i + 1
            continue
        line_list[i] = line_list[i] + str(temp)
    # 验证未被哈希的集合中有没有light_node_data,即第一行的数据是否存在
    flag = False
    count = 0
    line_count = 0
    # 从数组中找light node发来的测试样例,并加入对应哈希值到核心数组中
    for first_line_hash in line_list:
        if first_line_hash == light_node_hash:
            flag = True
            # line_count负责记录每行需要保存的核心数的索引值
            line_count = count
            break
        count = count + 1
    if flag == True:
        print('data has been saving')
    else:
        print('can not find data')
        return [],[]
    # 循环把每一行对应的记录进去,分count奇偶情况
    while line:
        # 数据处理部分
        line_list = []
        i = 0
        line_list.append('')
        for temp in line:
            if temp == '[' or temp == ']' or temp == "'" or temp == " " or temp == "\n":
                continue
            if temp == ',':
                line_list.append('')
                i = i + 1
                continue
            line_list[i] = line_list[i] + str(temp)
        # 索引偶数位置情况
        print(line_list)
        print(line_count)
        if line_count % 2 == 0:
            core_hash.append(line_list[line_count])
            neighbour_hash.append(line_list[line_count + 1])
        else:
            core_hash.append(line_list[line_count])
            neighbour_hash.append(line_list[line_count - 1])
        line = f.readline()
        line_count = line_count // 2
    f.close()
    # 打开root.txt，继续读取
    f = open('root.txt')
    line = f.readline()
    # 在root.txt中找对应子树的line_count
    line_list = []
    i = 0
    line_list.append('')
    for temp in line:
        if temp == '[' or temp == ']' or temp == "'" or temp == " " or temp == "\n":
            continue
        if temp == ',':
            line_list.append('')
            i = i + 1
            continue
        line_list[i] = line_list[i] + str(temp)

    flag = False
    count = 0
    line_count = 0
    for temps in line_list:
        if temps == hash_2(core_hash[-1], neighbour_hash[-1]) or temps == hash_2(neighbour_hash[-1],core_hash[-1]):
            flag = True
            # line_count负责记录每行需要保存的核心数的索引值
            line_count = count
            break
        count = count + 1
    if flag == True:
        print('ROOTdata has been saving')
    else:
        print('can not find data')
        return [], []

    while line:
        line_list = []
        i = 0
        line_list.append('')
        for temp in line:
            if temp == '[' or temp == ']' or temp == "'" or temp == " " or temp == "\n":
                continue
            if temp == ',':
                line_list.append('')
                i = i + 1
                continue
            line_list[i] = line_list[i] + str(temp)
        # 读取到根时候停止
        if len(line_list) == 1:
            core_hash.append(line_list[line_count])
            break
        if line_count % 2 == 0:
            core_hash.append(line_list[line_count])
            neighbour_hash.append(line_list[line_count + 1])
        else:
            core_hash.append(line_list[line_count])
            neighbour_hash.append(line_list[line_count - 1])
        line_count = line_count // 2
        line = f.readline()
    f.close()
    return core_hash,neighbour_hash

blockchain = Blockchain()
# 挖矿时是否要访问预言机
oracle_flag = False
# 根据网关等生成随机身份标识码
miner_self_identity=str(uuid.uuid4()).replace('-', '')
# mine_flag=False

app = Flask(__name__)

@app.route('/help',methods=['GET'])
def blockchain_help():
    response = {
        "help01": "How to get newest block chain",
        "01methods": "GET",
        "01url input": "/chain",
        "---------------": "----------------------",
        "help02": "How to add a new transaction",
        "02methods": "POST",
        "02url input": "/transactions/new",
        "02body options": "raw-json",
        "02body model": "{sender,recipient,amount}"
    }
    return jsonify(response),200

# 定义接收接收交易路由
@app.route('/transactions/new', methods=['POST'])
def transactions():
    values = request.get_json()
    checktype = ''
    if 'T-Type' in values:
        checktype = values['T-Type']
        blockchain.count_ttype_num(checktype)
    # print(checktype)
    # 记录究竟有多少个T-Type
    # print(blockchain.ttype)
    if checktype == 'dsrc':
        check = ['T-Type', 'Sender', 'Receiver', 'M-Type', 'Msg', 'Communication object']
        # 检查数据完整性
        if values is None:
            return 'Error:No Data input', 400
        if not all(k in check for k in values):
            return 'Missing Data input', 400
        # 写入区块对应位置
        index=blockchain.dsrc(values['T-Type'], values['Sender'], values['Receiver'], values['M-Type'], values['Msg'], values['Communication object'])
        response = 'We will add this transactions to block%s' % index
        return jsonify(response),201

    elif checktype == 'fees':
        check = ['T-Type', 'Sender', 'Receiver', 'M-Type', 'Msg', 'Fees']
        # 检查数据完整性
        if values is None:
            return 'Error:No Data input', 400
        if not all(k in check for k in values):
            return 'Missing Data input', 400
        # 写入区块对应位置
        index=blockchain.fees(values['T-Type'], values['Sender'], values['Receiver'], values['M-Type'], values['Msg'], values['Fees'])
        response = 'We will add this transactions to block%s' % index
        return jsonify(response),201

    elif checktype == 'trafficvio':
        check = ['T-Type', 'Sender', 'Receiver', 'License plate']
        # 检查数据完整性
        if values is None:
            return 'Error:No Data input', 400
        if not all(k in check for k in values):
            return 'Missing Data input', 400
        # 写入区块对应位置
        index=blockchain.traffic_vio(values['T-Type'], values['Sender'], values['Receiver'], values['License plate'])
        response = 'We will add this transactions to block%s' % index
        return jsonify(response),201
    # 本地找不到的情况，发送到预言机询问
    else:
        global oracle_flag
        oracle_flag = True
        headers = {'content-type': 'application/json'}
        rsuurl = 'http://127.0.0.1:8000/confirm_data'  # 修改，以及模板数据
        res = requests.post(url=rsuurl, data=json.dumps(values), headers=headers)
        return 'we need to ask oracle machine', 201


# 定义返回当前区块内容的路由
@app.route('/chain', methods=['GET'])
def chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response),200

# 自动挖矿，开启只需要访问该地址，并且设置flag
@app.route('/mine', methods=['GET'])
def mine():
    # 提醒预言机整理数据，返回整理好的数据，返回类型是一个list，里面为预言机函数的子树根值，由于本处减去网络延时的影响，去除txt文件传递
    global oracle_flag
    if oracle_flag == True:
        headers = {'content-type': 'application/json'}
        rsuurl = 'http://127.0.0.1:8000/backdata'  # 预言机返回数据地址
        res = requests.get(url=rsuurl)
        res_dict = json.loads(res.text)
        blockchain.merkle(res_dict)
    # 生成merkle树
    else:
        res_dict = []
        blockchain.merkle(res_dict)
    proof = blockchain.proof_of_work()
    # 激励机制
    # blockchain.dsrc(sender='0',recipient=miner_self_identity,amount=15)
    current_block= blockchain.new_block(proof, previous_hash=None)
    respone = {
        'message': 'A new block has been mined',
        'index': current_block['index'],
        'timestamp': current_block['timestamp'],
        'proof': current_block['proof'],
        'previous_hash': current_block['previous_hash'],
        'transactions': current_block['transactions'],
        'merkle': current_block['merkle'],
        'blcok_total_length': len(blockchain.chain)
    }
    blockchain.ttype = []
    return jsonify(respone),200

# #控制挖矿开始/停止的flag标志设置
# @app.route('/mine/flagset',methods=['POST'])
# def flag_set():
#     #得到并解析json数据
#     value=request.get_data()
#     value = json.loads(value)
#     bool_value=bool(value)
#     if bool_value==False:
#         mine_flag=False
#     else:
#         mine_flag=True
#     return 'flag has benn set',201



# 节点注册 输入数据格式 'nodes':['http;//127.0.0.2:5001',]
@app.route('/node/register',methods=['POST'])
def node_register():
    values = request.get_json()
    if values is None:
        return 'None data input',400
    nodes = values.get('nodes')
    for node in nodes:
        blockchain.register_node(node)
    response={
        "message":"nodes add successfully",
        "total nodes":list(blockchain.nodes)
    }
    return jsonify(response),201

# 区块链冲突解决
@app.route('/conflict/resolve',methods=['GET'])
def conflict_resolve():
    oldindex = blockchain.last_block['index']
    judgement = blockchain.resolve_conflict()
    if judgement is False:
        response = {
            "message": "we are the right chain",
            "old_index": oldindex,
            "newest_index": blockchain.last_block['index']
        }
    else:
        response={
            "message": "we have replaced newest chain",
            "old_index": oldindex,
            "newest_index": blockchain.last_block['index']
        }
    return jsonify(response), 200

#这里设定的功能只能查询上一个区块的某个交易
@app.route('/transaction/check1',methods=['POST'])
def transaction_check1():
    values = request.get_json()
    checktype = values['T-Type']
    if values is None:
        return 'None data input',400
    core_list,neighbour_list = readtxt1(checktype, values)
    response = {
        "core_list":core_list,
        "neighbour_list":neighbour_list
    }

    return jsonify(response),200

@app.route('/transaction/check2',methods=['POST'])
def transaction_check2():
    values = request.get_json()
    checktype = values['T-Type']
    if values is None:
        return 'None data input',400
    core_list,neighbour_list = readtxt2(checktype, values)
    response = {
        "core_list":core_list,
        "neighbour_list":neighbour_list
    }

    return jsonify(response),200

@app.route('/transaction/check3',methods=['POST'])
def transaction_check3():
    values = request.get_json()
    checktype = values['T-Type']
    if values is None:
        return 'None data input',400
    core_list,neighbour_list = readtxt3(checktype, values)
    response = {
        "core_list":core_list,
        "neighbour_list":neighbour_list
    }

    return jsonify(response),200

#----------------------------------函数-------------------------------------------


if __name__=='__main__':
    # 输入port入口
    # 启动项
    parser=ArgumentParser()
    # 设定运行格式python xxx.py -p/-port,help提示在python xxx.py -h 会出现
    parser.add_argument('-p', '--port', default=5000, help='input your using port')
    # 解析输入的参数
    args=parser.parse_args()
    # args.xxx   xxx由设定参数-port确定
    port=args.port

    app.run(host='0.0.0.0', port=port, debug=True)
