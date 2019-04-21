from flask import Flask, render_template, request, url_for
import pandas as pd
import numpy as np
import csv
from pca_data_prepare import *
np.set_printoptions(suppress=True)
import json
app = Flask(__name__)

@app.route("/linechart", methods=['GET', 'POST'])
def linechart():
    application_name = "pmd"
    data = pd.read_csv(application_name + ".csv")
    latency_90 = list(data["latency90"])
    latency_90 = [round(i, 2) for i in latency_90]
    timeseries = list(data["date"])
    timeseries = [i.split(" ")[1].split(".")[0] for i in timeseries]
    header = ["BW","MEM_BW","switch","cpu","io","memory","network"]
    header2 = ["id"] + header
    date = "3/28/2019 "
    if request.method == "POST":
        rec_time_all = json.loads(request.form["time"])
        data = get_range_data(rec_time_all, date, data)
        new_bar_chart = get_pca_components_range(data, header, application_name)
        print (new_bar_chart)
        new_m = get_correlation_table(application_name, header, data)
        new_parallel_data, ratio_header, new_components = get_parallel_json_data(data, header, application_name)
        print (new_parallel_data)

        respon_mess = {"new_correlation_matrix": new_m, "new_parallel_data": new_parallel_data, "new_header": header2,
                       "new_parallel_header": header, "new_eigen_header": ratio_header, "new_barchart_header": header,
                       "new_barchart_data": new_components}
        return json.dumps(respon_mess)
    
    raw_data = data
    matrix_json = get_correlation_table(application_name, header, raw_data)
    parallel_data, ratio_header, components = get_parallel_json_data(raw_data, header, application_name)
    return render_template("linechart.html", latency_90={"latency_90": latency_90}, timeseries={"timeseries": timeseries},
                           application_name=application_name,#line chart
                           correlation_matrix={"correlation_matrix": matrix_json},
                           correlation_header={"correlation_header": header2},#correlation table
                           parallel_data=parallel_data,
                           parallel_header={"parallel_header": header},#parallel coordinator
                           eigen_header={"eigen_header": ratio_header},
                           barchart_header={"barchart_header": header}, #barchart
                           barchart_data={"barchart_data": components}
                           )

def get_components_from_data(data, header):
    eigenvector, ratio, components = get_pca_data(data, header)
    components = components[:2].tolist()
    components[0] = [round(i, 2) for i in components[0]]
    components[1] = [round(i, 2) for i in components[1]]
    return components

def get_pca_components_range(data, header, application_name):
    target_name = "parallel_" + application_name + ".csv"
    return_value = {}
    if data.empty == False:
        return_value["all_selected"] = get_components_from_data(data, header)
        for range_name in ['range1', 'range2', 'common_range']:
            d_r = data[data.range == range_name]
            if d_r.empty == False:
                return_value[range_name] = get_components_from_data(d_r, header)
    return return_value

def get_range_data(rec_time_all, date, data):
    rec_time_a = rec_time_all["all_select_range"]
    start_time = date + rec_time_a[0]
    end_time = date + rec_time_a[1]
    data['date'] = pd.to_datetime(data['date'])
    data['range'] = "None"
    data = data.set_index('date')
    data = data[start_time:end_time]
    for r in ["range1", "range2", "common_range"]:
        var_range = rec_time_all[r]
        if (len(var_range) > 0):
            var_range_s = date + var_range[0]
            var_range_e = date + var_range[1]
            data.loc[var_range_s: var_range_e, 'range'] = r

    if (len(rec_time_all["range1"]) == 0 and len(rec_time_all["range2"]) == 0 and len(
            rec_time_all["common_range"]) == 0):
        data['range'] = "all"
    data = data.reset_index()
    data = data[data.range != "None"]
    data = data.reset_index(drop=True)
    return data

def get_correlation_table(application_name, header, raw_data):
    header2 = ["id"] + header
    get_correlation_csv(application_name, raw_data)
    data = pd.read_csv('correlation_'+ application_name + '.csv')

    matrix = []
    first_1 = 1
    loc_index = 0
    for loc_index in range(0, len(data)):
        tmp_d = data.loc[loc_index].tolist()
        tmp_d = [str(i) for i in tmp_d]
        tmp_d[0] = header[loc_index]
        for i in range(first_1 + 1, len(tmp_d)):
            tmp_d[i] = [list(raw_data[tmp_d[0]]), list(raw_data[header[i-1]])]
        matrix.append(tmp_d)
        first_1 += 1
    matrix_json = []

    for loc_index in range(0, len(matrix)):
        m_i = 0
        json_data = {}
        for d in matrix[loc_index]:
            json_data[header2[m_i]] = d
            m_i += 1
        matrix_json.append(json_data)
    return matrix_json

def get_correlation_csv(application_name, raw_data):
    dataset = raw_data
    drop_attr = ['date', 'DISTSIM_BENCH.benchmark_id', 'L2_BW', 'L3_BW',
                           'latency', 'latency90']
    if 'range' in dataset.columns:
        drop_attr.append('range')
    subset = dataset.drop(drop_attr, axis=1)
    data = subset.values
    result = np.corrcoef(data, rowvar=0)
    result = np.around(result, decimals=2)
    df = pd.DataFrame(result)
    target_name = "correlation_" + application_name + ".csv"
    df.to_csv(target_name)
    return 0

def get_parallel_data(raw_data, header, application_name): #raw_data: dataframe
    target_name = "parallel_" + application_name + ".csv"
    eigenvector, ratio, components = get_pca_data(raw_data, header)
    df_date = raw_data.date
    df2 = raw_data.drop(["date", "DISTSIM_BENCH.benchmark_id", "L2_BW", "L3_BW", "latency"],axis=1)
    df1 = pd.DataFrame(eigenvector)
    df1.columns = ratio
    df_all = pd.concat([df1, df2, df_date], axis=1, ignore_index=False)
    df_all.to_csv(target_name, index=None)
    b = list(csv.reader(open(target_name)))
    data = b[1:]
    h = b[0]
    components = components[:2].tolist()
    components[0] = [round(i, 2) for i in components[0]]
    components[1] = [round(i, 2) for i in components[1]]
    return data, h, ratio, components

def get_parallel_json_data(raw_data, header, application_name):
    data = raw_data
    d, h, ratio, components= get_parallel_data(data, header, application_name)
    parallel_data = []
    id = 0
    for item in d:
        tmp = {}
        for i in range(0, len(item)):
            tmp[h[i]] = item[i]
        tmp["id"] = id
        parallel_data.append(tmp)
        id += 1
    print ("ratio")
    print (ratio)
    return {"parallel_data":parallel_data}, ratio, components

if __name__ == '__main__':

    app.run()