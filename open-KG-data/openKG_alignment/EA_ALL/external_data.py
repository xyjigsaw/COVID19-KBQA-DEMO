# Name: external_data
# Author: Reacubeth
# Time: 2020/3/28 14:03
# Mail: noverfitting@gmail.com
# Site: www.omegaxyz.com
# *_*coding:utf-8 *_*

import json
import csv
import pandas as pd

def count_al(string):
    a = 0
    for i in string:
        if i.isalpha():
            a += 1
    return a

class_ls = []
class_id = []
class_type = []
class_name = []

resource_ls = []
resource_id = []
resource_type = []
resource_name = []

property_ls = []
property_id = []
property_type = []
property_name = []

others_ls = []


with open("科研rdf type.txt", "r", encoding='utf-8') as f:  # 打开文件
    data = json.loads(f.read())  # 读取文件

data = data['data']['results']['bindings']

for item in data:
    print(item)
    if 'resource' in item['x']['value'].lower():
        if item['x']['value'] not in resource_id:
            resource_id.append(item['x']['value'])
            resource_type.append('http://www.openkg.cn/COVID-19/health/class/')
            resource_name.append(item['label']['value'])
        else:
            idx = resource_id.index(item['x']['value'])
            if count_al(item['label']['value']) < count_al(resource_name[idx]):
                resource_name[idx] = item['label']['value']

    elif 'class' in item['x']['value'].lower():
        if item['x']['value'] not in class_id:
            class_id.append(item['x']['value'])
            class_type.append('rdf-schema:Class')
            class_name.append(item['label']['value'])
        else:
            idx = class_id.index(item['x']['value'])
            if count_al(item['label']['value']) < count_al(class_name[idx]):
                class_name[idx] = item['label']['value']
    elif 'property' in item['x']['value'].lower():
        if item['x']['value'] not in property_id:
            property_id.append(item['x']['value'])
            property_type.append('http://www.w3.org/1999/02/22-rdf-syntax-ns#Property')
            property_name.append(item['label']['value'])
        else:
            idx = property_id.index(item['x']['value'])
            if count_al(item['label']['value']) < count_al(property_name[idx]):
                property_name[idx] = item['label']['value']


dataframe = pd.DataFrame({'id': class_id, 'type': class_type, 'name': class_name})
dataframe.to_csv(r"research_class_ext.csv", sep=',', index=False)

dataframe = pd.DataFrame({'id': resource_id, 'type': resource_type, 'name': resource_name})
dataframe.to_csv(r"research_resource_ext.csv", sep=',', index=False)

dataframe = pd.DataFrame({'id': property_id, 'type': property_type, 'name': property_name})
dataframe.to_csv(r"research_property_ext.csv", sep=',', index=False)