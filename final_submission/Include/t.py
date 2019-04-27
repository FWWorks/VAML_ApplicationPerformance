import pandas as pd
import numpy as np
from pca_data_prepare import *
import csv

header = ["BW", "MEM_BW", "switch", "cpu", "io", "memory", "network"]
data = pd.read_csv("testbug.csv")

def get_parallel_data(raw_data, header, application_name): #raw_data: dataframe
    target_name = "parallel_" + application_name + ".csv"
    eigenvector, ratio = get_pca_data(raw_data, header)
    df2 = raw_data.drop(["date", "DISTSIM_BENCH.benchmark_id", "L2_BW", "L3_BW", "latency"],axis=1)
    df1 = pd.DataFrame(eigenvector)
    df1.columns = ratio
    df_all = pd.concat([df1, df2], axis=1, ignore_index=False)
    df_all.to_csv(target_name, index=None)
    b = list(csv.reader(open(target_name)))
    data = b[1:]
    h = b[0]
    return data, h, ratio

def get_parallel_json_data(raw_data, header, application_name):
    data = raw_data
    d, h, ratio= get_parallel_data(data, header, application_name)
    parallel_data = []
    id = 0
    for item in d:
        tmp = {}
        for i in range(0, len(item)):
            tmp[h[i]] = item[i]
        tmp["id"] = id
        parallel_data.append(tmp)
        id += 1
    return {"parallel_data":parallel_data}, ratio

new_parallel_data, ratio_header = get_parallel_json_data(data, header, "pmd")
print (new_parallel_data)