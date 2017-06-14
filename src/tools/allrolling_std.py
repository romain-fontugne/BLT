import numpy as np

def allrolling_std(data, window):
    mean = list()
    median = list()
    std = list()

    time = len(data[0])
    for t in range(time-window+1):
        tmp = list()
        for an in data:
            for value in an[t:t+window]:
                if value == "-":
                    continue
                tmp.append(value)
        
        mean.append(np.mean(tmp))
        median.append(np.median(tmp))
        std.append(np.std(tmp))
    return [mean, median, std]

if __name__ == "__main__":
    windows = 4

    x = [0,1,2,3,4,5,6]
    y = [[0,2,3,4,5,6,7], [4,3,5,6,7,8,7], [4,5,6,3,4,5,6], [3,4,5,2,4,5,7]]
    print allrolling_std(y, windows)

    y_ = list()
    x_ = list()
    mean = list()
    median = list()
    mean_ = list()
    median_ = list()
    for t in range(len(y[0])):
        for i in range(len(y)):
            if len(x_)-1 != t:
                x_.append(list())
            x_[t].append(y[i][t])
    a = np.ones(windows)/windows
    for i in x_:
        mean.append(np.mean(i))
        median.append(np.median(i))
    mean_.append(np.convolve(mean, a, "valid"))

    print list(mean_)
    print list(median_)
