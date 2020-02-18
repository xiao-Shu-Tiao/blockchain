
#

#
#     # for j in temp_list:
#
# # for i in range(5):
# #     exec('var{} = {}'.format(i, i))
# # print(var0, var1, var2, var3 ,var4)
# exec('ttypelist{} = {}'.format(1, 1))
# print(ttypelist1)
# # ttypelistdsrc = []
# # check_ttype = 'dsrc'
# # exec('ttypelist{}.append(var1)'.format(check_ttype))
# # print(ttypelistdsrc)
# # exec('a=len(ttypelistdsrc)')
# # print(a)
# # for x in exec('ttypelist{}'.format(check_ttype)):
# #     print(x)
# # print(exec('len(ttypelist{})'.format(check_ttype)))
#
# var1 = {"T-Type":"dsrc", "Sender":"a", "Receiver":"b", "M-Type":"res", "Msg":"5a8c0f7e", "Communication object":"V2V"}
# var2 = {"T-Type":"fees", "Sender":"a", "Receiver":"b", "M-Type":"res", "Msg":"5a8c0f7e", "FEES":10}
# var3 = {"T-Type":"dsrc", "Sender":"a", "Receiver":"b", "M-Type":"res", "Msg":"5a8c0f7e", "Communication object":"V2V"}
# current_transactions = []
# current_transactions.append(var1)
# current_transactions.append(var2)
# current_transactions.append(var3)
# c =1
# class Test:
#     rq = None
#     def __init__(self):
#         pass
#
#     # def func(self):
#     #     exec('self.{}=[]'.format('fee'))
#     #     print(self.fee)
#
#     def make_ttype_list(self,current_transactions):
#         temp_list = []
#         self.ttypelistdsrc= 1
#         #  把所有不同的T-TYPE类型读取到数组中
#         for i in current_transactions:
#             ttypeproperty = i.get('T-Type')
#             if not ttypeproperty in temp_list:
#                 temp_list.append(ttypeproperty)
#         print(temp_list)
#         exec('self.'+'%s = []'%temp_list[0])
#         exec('self.'+'%s'%temp_list[0]+'1 = []')
#         self.dsrc.append(1)
#         print(self.dsrc)
#         print(self.dsrc1)
#         self.dsrc1 = self.dsrc
#         print(self.dsrc1)
#         exec('self.' + '%s.append(10)' % temp_list[0])
#         print(self.dsrc)
#         exec('self.temp = self.'+ '%s'%temp_list[0])
#         print(self.temp)
#         self.temp.append(100)
#         print(self.temp)
#         print(self.dsrc)
        # self.aa = 10
        # self.b = 0
        # exec('self.aa = self.b')
        # print(self.aa)

        #b = a

        # name = self.dsrc
        # exec('name=self.dsrc')
        # print(name)


#print(b)
# t1 = Test()
# t1.func()
# t1.make_ttype_list(current_transactions)



# exec('name=t1.dsrc')
# print(name)
# Test.sj = '15:30'
# print(t1.fee)
# class a():
#      def merkle(self):
#         self.temp_leaf = []
#         self.temp_hash = []
#         for cur_ttype in range(5):
#             # self.temp_leaf指向self.ttypelistdsrc等交易的地址
#             exec('self.temp_leaf = self.ttypelist' + 'cur_ttype')
#             # self.temp_hash指向self.hash_ttypelist等副本地址
#             exec('self.temp_hash = self.hash_ttypelist' + 'cur_ttype')
#             # 计算叶子节点哈希值
#             print(self.temp_leaf)
#             print(self.temp_hash)

# a=[1,2,3,4,5,6]
# a = a[0:1]
#
# print(a)

# a = [1, 2, 3, 4]
# b = a
# b = b[0:1]
# print(b)
# print(a)

# class a():
#     def __init__(self):
#         self.a = [1,2,3]
#
#     def func(self):
#         self.b = self.a
#         print(self.b)
#
# a1 = a()
# a1.func()
# test1 = ['dsrc','dsrc']
# test2 = ['dsrc']
# for i in test1:
#     for j in test2:
#         if i is j:
#             print('ok')
# print(5%2)

# import time
# startTimeStamp=time.time()
# for i in range(1,100):
#     print(i)
# endTimeStamp=time.time()
# print(endTimeStamp-startTimeStamp)


# cur_ttype = 'dsrc'
# temp_leaf = {
#     "T-Type":"dsrc",
#     "Sender":"a",
#     "Receiver":"b",
#     "M-Type":"res",
#     "Msg":"5a8c0f7e",
#     "Communication object":"v2v"
# }
# a = [1,2,3,4,5]
# # if cur_ttype == 'dsrc':
# #     exec("file = open('{}transaction.txt','a')".format(cur_ttype))
# file = open('transactions.txt','w')
# print(file)
# file.write(str(temp_leaf)+'\n')
# file.close()
#
# file = open('transactions.txt','a')
# file.write(str(a)+'\n')
# file.close()
# a = [1,2,3]
# b = [4,5]
# a+=b
# print(a)

# file = open('root.txt', 'r')
# a = file.readlines()
# # lists = []
# # for fields in a:
# #     fields=fields.strip("'[]'")
# #     fields=fields.split("','")
# #     lists.append(fields)
# print(a)
# a = file.readline()
# b = list(a)
# print(b)
# a = file.readline()
# print(a)
# a = file.readline()
# print(a)
# file.close()
# import hashlib
# import json
#
#

#
#
# def merkle_hash_2(data1, data2):
#     data = '%s%s' % (data1, data2)
#     json_string = json.dumps(data, sort_keys=True).encode()
#     # print('//hash 2: %s' % hashlib.sha256(json_string).hexdigest())
#     return hashlib.sha256(json_string).hexdigest()

# # 子树哈希值验证
# f = open('dsrctransaction.txt','r')
# # 读取文件行数
# # linelength = len(f.readlines())
# line = f.readline()
# last_list = []
# last_list.append('')
# i = 0
# for temp in line:
#     if temp == '[' or temp == ']' or temp == "'" or temp == " " or temp == "\n":
#         continue
#     if temp == ',':
#         last_list.append('')
#         i = i+1
#         continue
#     last_list[i] = last_list[i]+ str(temp)
# print(last_list)
#
# # for x in last_list:
# #     line = f.readline()
#
# f.close()

# 读取文件行数
# j = 3
# while j:
#     f = open('root.txt', 'r')
#     # if len(f.readlines()) == 1:
#     #     break
#     line = f.readline()
#     previous_list = []
#     previous_list.append('')
#     # print(line)
#     i = 0
#     for temp in line:
#         if temp == '[' or temp == ']' or temp == "'" or temp == " " or temp == "\n":
#             continue
#         if temp == ',':
#             previous_list.append('')
#             i = i+1
#             continue
#         previous_list[i] = previous_list[i] + str(temp)
#     print(previous_list)
#     j = j -1
#     f.close()
# a=[1,2,3,4]
# print(a.index(3))
# i = 0
# while i<10:
#     print(i)
#     for j in range(1,3):
#         print('ok')
#         if j == 3:
#             break
#     i = i + 1
# a = 3 // 2
# print(a)
# for i in range(1,3):
#     print(1)
# import os
# print(os.path.exists("test.py"))
# import json
# import hashlib
# import requests
# headers = {'content-type': 'application/json'}
# rsuurl = 'http://127.0.0.1:8000/backdata'  # 修改，以及模板数据
#
# res = requests.get(url=rsuurl)
# res_dict = json.loads(res.text)
# print(res_dict)
import json
import hashlib
#
# def hash_2(data1, data2):
#     data = '%s%s' % (data1, data2)
#     json_string = json.dumps(data, sort_keys=True).encode()
#     # print('//hash 2: %s' % hashlib.sha256(json_string).hexdigest())
#     return hashlib.sha256(json_string).hexdigest()
#
# a = hash_2('06ed5100b036ec3cfa84c09e62eff60ad4acd94d0b41a4d19f5ad0e7cc8da5e8', 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff')

def merkle_hash_1(data):
    json_string = json.dumps(data, sort_keys=True).encode()
    # print('//hash 1: %s' % hashlib.sha256(json_string).hexdigest())
    return hashlib.sha256(json_string).hexdigest()
a = merkle_hash_1('-ack -connect')
print(a)