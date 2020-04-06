# Name: fusion
# Author: Reacubeth
# Time: 2020/3/28 9:33
# Mail: noverfitting@gmail.com
# Site: www.omegaxyz.com
# *_*coding:utf-8 *_*

import csv
import pandas as pd


def count_al(string):
    a = 0
    for i in string:
        if i.isalpha():
            a += 1
    return a


sFileName = 'abbr_data_all.csv'


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

with open(sFileName, newline='', encoding='UTF-8') as f:
    rows = csv.reader(f)
    for row in rows:
        if 'class' in row[0].lower():
            class_ls.append(row[:-1])
            if row[0].strip().replace('"', '') not in class_id:
                class_id.append(row[0].strip().replace('"', ''))
                class_type.append(row[1].strip().replace('"', ''))
                class_name.append(row[2].strip().replace('"', ''))
            else:
                idx = class_id.index(row[0].strip().replace('"', ''))
                if count_al(row[2].strip().replace('"', '')) < count_al(class_name[idx]):
                    class_name[idx] = row[2].strip().replace('"', '')
        elif 'resource' in row[0].lower():
            resource_ls.append(row[:-1])
            if row[0].strip().replace('"', '') not in resource_id:
                resource_id.append(row[0].strip().replace('"', ''))
                resource_type.append(row[1].strip().replace('"', ''))
                resource_name.append(row[2].strip().replace('"', ''))
            else:
                idx = resource_id.index(row[0].strip().replace('"', ''))
                if count_al(row[2].strip().replace('"', '')) < count_al(resource_name[idx]):
                    resource_name[idx] = row[2].strip().replace('"', '')
        elif 'property' in row[0].lower():
            property_ls.append(row[:-1])
            if row[0].strip().replace('"', '') not in property_id:
                property_id.append(row[0].strip().replace('"', ''))
                property_type.append(row[1].strip().replace('"', ''))
                property_name.append(row[2].strip().replace('"', ''))
            else:
                idx = property_id.index(row[0].strip().replace('"', ''))
                if count_al(row[2].strip().replace('"', '')) < count_al(property_name[idx]):
                    property_name[idx] = row[2].strip().replace('"', '')
        else:
            others_ls.append(row[:-1])
            print('bad source detected!')


dataframe = pd.DataFrame({'id': class_id, 'type': class_type, 'name': class_name})
dataframe.to_csv(r"class_all.csv", sep=',', index=False)

dataframe = pd.DataFrame({'id': resource_id, 'type': resource_type, 'name': resource_name})
dataframe.to_csv(r"resource_all.csv", sep=',', index=False)

dataframe = pd.DataFrame({'id': property_id, 'type': property_type, 'name': property_name})
dataframe.to_csv(r"property_all.csv", sep=',', index=False)