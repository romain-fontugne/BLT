import pandas as pd
from matplotlib import pyplot as plt

def convert_list_pd(y):
    y_pandas = pd.DataFrame()
    for y_ in y:
        l = list()
        for w in range(len(y_)):
            l.append(y_[w])
        y_pandas = y_pandas.append(pd.DataFrame([l], columns=[0,1,2]), ignore_index=True)
    return y_pandas

def allrolling_std(window, data):
    std = list()
    avg = list()
    nrow, ncolumn = data.shape
    for i in range(nrow-(window-1)):
        data_ = pd.DataFrame()
        for w in range(ncolumn):
            data_ = pd.concat([data_, data.ix[i:i+(window-1),w]], axis=0, ignore_index=True)
        std.append(data_.std())
        avg.append(data_.mean())
    return [std, avg]

windows = 4

x = [1,2,3,4,5,6,7,8,9]
y = [[2,3,4], [1,2,3], [5,6,7], [1,2,3], [2,3,4], [5,3,4], [1,5,4], [4,2,3], [5,7,6]]
y_pandas = convert_list_pd(y)
print y_pandas
print allrolling_std(windows, y_pandas)
