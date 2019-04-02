from flask import Flask, render_template, request, url_for
import pandas as pd
import numpy as np
import os
from pca_data_prepare import *
np.set_printoptions(suppress=True)
import json
app = Flask(__name__)
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
print (SITE_ROOT)
from flask_cors import CORS
CORS(app)

short_name = {
    "DISTSIM_BENCH.host_L3_SYSTEM_BW": "L3_BW",
    "DISTSIM_BENCH.host_MEM_BW": "MEM_BW",
    "DISTSIM_BENCH.host_context_switch": "C_S",
    "DISTSIM_BENCH.host_cpupercent": "CPU",
    "DISTSIM_BENCH.host_disk_io" : "IO",
    "DISTSIM_BENCH.host_memory": "MEM",
    "DISTSIM_BENCH.host_network": "NET"

}
drop_attr = ['date', 'DISTSIM_BENCH.benchmark_id', 'DISTSIM_BENCH.host_L2_BW', 'DISTSIM_BENCH.host_L3_BW',
                           'DISTSIM_BENCH.latency', 'DISTSIM_BENCH.latency90']
metrics = ['DISTSIM_BENCH.host_L3_SYSTEM_BW', 'DISTSIM_BENCH.host_MEM_BW', 'DISTSIM_BENCH.host_context_switch', 'DISTSIM_BENCH.host_cpupercent',
           'DISTSIM_BENCH.host_disk_io', 'DISTSIM_BENCH.host_memory', 'DISTSIM_BENCH.host_network']
@app.route("/")
def hello():
    data = pd.read_csv('correlation.csv')
    raw_data = pd.read_csv('dataset.csv')

    header = ["A", "B", "C", "D", "E", "F", "G"]
    header2 = ["id"] + header
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

    return render_template("t.html", correlation_matrix={"correlation_matrix": matrix_json}, correlation_header={"correlation_header": header2})

@app.route("/a", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        name = request.form["name"]
        return json.dumps({"aa":[10, 8, 6, 5]})
        #return name + " Hello"

    return render_template("linktest.html")

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
        rec_time = request.form["time"]
        start_time = date + rec_time.split(",")[0]
        end_time = date + rec_time.split(",")[1]
        data['date'] = pd.to_datetime(data['date'])
        data = data.set_index('date')
        data = data[start_time:end_time]
        data = data.reset_index()
        new_m = get_correlation_table(application_name, header, data)
        for m in new_m:
            print (m)
        respon_mess = {"new_correlation_matrix": new_m, "new_header": header2, "time_start_end": rec_time}
        return json.dumps(respon_mess)
    parallel_url = os.path.join(SITE_ROOT, "parallel_"+ application_name+ ".csv")
    raw_data = data
    matrix_json = get_correlation_table(application_name, header, raw_data)
    return render_template("linechart.html", latency_90={"latency_90": latency_90}, timeseries={"timeseries": timeseries},
                           application_name=application_name,#line chart
                           correlation_matrix={"correlation_matrix": matrix_json},
                           correlation_header={"correlation_header": header2},#correlation table
                           parallel_url=parallel_url

                           )

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
    eigenvector, ratio = get_pca_data(raw_data, header)
    df2 = raw_data.drop(["date", "DISTSIM_BENCH.benchmark_id", "L2_BW", "L3_BW", "latency", "latency90"],axis=1)
    df1 = pd.DataFrame(eigenvector)
    df1.columns = ratio
    df_all = pd.concat([df1, df2], axis=1, ignore_index=False)
    df_all.to_csv(target_name, index=None)
    return 0

if __name__ == '__main__':
    app.run()