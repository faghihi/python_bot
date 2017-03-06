from openpyxl import load_workbook
import numpy as np


def initialize():
    wb = load_workbook(filename='test.xlsx')
    sheet_ranges = wb['پست']

    items = [item.value for item in list(sheet_ranges['1'])]
    cols = sheet_ranges.columns
    dic = {}
    for item in cols:
        listt = []
        key = item[0].value
        for t in item:
            if (t.value != key and t.value != None):
                listt.append(t.value)
        dic[key] = listt

    return dic


def keyboard_generate(value, n):
    if int(n * 2) == len(value):
        return (np.array(value).reshape((n, 2))).tolist()
    else:
        ls = np.array(value[:len(value) - 1]).reshape((len(value) - 1)/2, 2).tolist()
        ls.append([value[len(value) - 1]])
        return ls
