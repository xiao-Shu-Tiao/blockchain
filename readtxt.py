import hashlib
import json



def hash_2(data1, data2):
    data = '%s%s' % (data1, data2)
    json_string = json.dumps(data, sort_keys=True).encode()
    # print('//hash 2: %s' % hashlib.sha256(json_string).hexdigest())
    return hashlib.sha256(json_string).hexdigest()


prev_list = []
last_list = []

f = open("dsrctransaction.txt")
line = f.readline()
i = 0
prev_list.append('')
for temp in line:
    if temp == '[' or temp == ']' or temp == "'" or temp == " " or temp == "\n":
        continue
    if temp == ',':
        prev_list.append('')
        i = i+1
        continue
    prev_list[i] = prev_list[i] + str(temp)
print(prev_list)

line = f.readline()
i = 0
last_list.append('')
for temp in line:
    if temp == '[' or temp == ']' or temp == "'" or temp == " " or temp == "\n":
        continue
    if temp == ',':
        last_list.append('')
        i = i+1
        continue
    last_list[i] = last_list[i] + str(temp)
print(last_list)

while line:
    # 数据比较部分
    count = 0
    prev_length = len(prev_list)
    last_length = len(last_list)
    while count != last_length:
        # print('prev_list is %s %s'%(prev_list[2*count],prev_list[2*count]))
        prev_data = hash_2(prev_list[2*count],prev_list[2*count+1])
        # print('prevdata is :%s',str(prev_data))
        if str(prev_data) == last_list[count]:
            print('equal')
        count = count + 1

    # 数据置换部分
    prev_list = last_list
    line = f.readline()
    if line == '':
        break
    last_list = []

    # last数据处理
    i = 0
    last_list.append('')
    for temp in line:
        if temp == '[' or temp == ']' or temp == "'" or temp == " " or temp == "\n":
            continue
        if temp == ',':
            last_list.append('')
            i = i + 1
            continue
        last_list[i] = last_list[i] + str(temp)
    print(prev_list)
    print(last_list)
f.close()


