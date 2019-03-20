from flask import Flask, render_template, request
import pandas as pd
import csv
import json
import re
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

def get_z(selected_name, metrics, data_json, ts):
    a = data_json
    filtered_data = []
    selected_name = "redis"
    z_value = []
    a = json.loads(a)
    for i in a:
        if i["name"] == selected_name and i["time"] in ts:
            filtered_data.append(i)

    for m in metrics:
        tmp = []
        for i in filtered_data:
            if m in i.keys():
                tmp.append(i[m])
            # tmp1.append({"metric": m, "data": tmp})
        z_value.append(tmp)
    return z_value


def get_times(selected_name, data_json):
    a = json.loads(data_json)
    t = []
    for i in a:
        if i["name"] == selected_name:
            t.append(i["time"])
    return t


def get_model(DATA_FILE, FEAT_COLS, NAME):
    data = pd.read_csv(DATA_FILE, usecols=FEAT_COLS + ['latency90', 'name'])
    data = data[data.name == NAME]
    data = data.drop(columns=['name'])

    X = data[FEAT_COLS].values  # get features
    y = data['latency90'].values  # get performance

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1 / 3, random_state=22)

    linear_reg_model = LinearRegression()
    linear_reg_model.fit(X_train, y_train)
    r2_score = linear_reg_model.score(X_test, y_test)
    print(r2_score)

    return linear_reg_model, X


@app.route('/')
def index():
    return render_template("helloworld.html")

@app.route('/drop',methods=['GET','POST'])
def droptest():
    data = pd.read_csv('timeseries.csv')
    metrics = ["CPI", "BW", "L3_BW", "LLC"]
    names = set(data["name"])
    default_selected_metrics = metrics
    default_selected_names = data["name"].tolist()[0]
    if request.method == "POST":
        selected_metircs = request.form.getlist("metrics")
        selected_names = request.form.getlist("names")
        if selected_metircs!=None and selected_names!=None:
            print (selected_metircs)
            return render_template("droptest.html", metrics=metrics, selected_metircs = {"metrics": selected_metircs},
                                   names = names, selected_names = {"names": selected_names})
    return render_template('droptest.html', metrics=metrics, names=names, selected_metircs = {"metrics": default_selected_metrics},
                           selected_names={"names": default_selected_names})

def get_linechart_data(selected_names,  metrics, a):
    metrics_value = []
    filter_data = []
    for i in a:
        if i["name"] == selected_names:
            #times_all.append(i["time"])
            filter_data.append(i)

    for m in metrics:
        tmp = []
        for i in filter_data:
            tmp.append((i[m]))
        metrics_value.append(tmp)
    return metrics_value


@app.route('/ts',methods=['GET','POST'])
def tstest():
    data = pd.read_csv('timeseries.csv')
    data_json = data.to_json(orient='records')
    metrics = ['CPI', 'BW', 'L3_BW', 'L2_BW', 'MEM_BW', 'client']
    names = set(data["name"])
    default_selected_metrics = ['CPI', 'BW', 'L3_BW', 'L2_BW', 'MEM_BW']
    default_algorithm = ["LR", "RNN"]
    default_selected_names = data["name"].tolist()[0]
    times = get_times(default_selected_names, data_json)
    z_value = get_z(default_selected_names, default_selected_metrics, data_json, times)
    metrics_value = get_linechart_data(default_selected_names, ["latency90"], json.loads(data_json))

    DATA_FILE = 'timeseries.csv'
    FEAT_COLS = default_selected_metrics
    NAME = default_selected_names
    linear_reg_model, X = get_model(DATA_FILE, FEAT_COLS, NAME)
    lr_prediction = []
    for x in X:
        lr_prediction.append(linear_reg_model.predict([x])[0])

    print (len(metrics_value))
    print(lr_prediction)



    if request.method == "POST":
        selected_metrics = request.form.getlist("metrics")
        selected_names = request.form.getlist("names")
        selected_algorithms = request.form.getlist("algorithms")
        algorithm_selected = selected_algorithms[0]
        times = get_times(selected_names[0], data_json)

        if selected_metrics != None and selected_names != None:
            print(selected_metrics)
            print(selected_names[0])
            print(algorithm_selected)
            print (times)
            z_value = get_z(selected_names[0], selected_metrics, data_json, times)

            metrics_value = get_linechart_data(selected_names[0], selected_metrics, json.loads(data_json))
            m_v_2 = get_linechart_data(selected_names[0], selected_metrics+["latency90"], json.loads(data_json))
            return render_template("timeseries_view.html", metrics=metrics, selected_metrics={"metrics": selected_metrics+["latency90"]},
                                   names=names, selected_names={"names": selected_names}, name=selected_names,
                                   feathername={"fn": selected_metrics}, zvalue={"z": z_value}, times={"t": times},metricsvalue={"m_v": m_v_2},
                                   selected_algorithms={"algorithms": algorithm_selected}, algorithms=default_algorithm, lr_pred={"lr": lr_prediction})

    return render_template('timeseries_view.html', metrics=metrics, names=names, algorithms=default_algorithm,
                           selected_metrics={"metrics": default_selected_metrics},
                           selected_names={"names": default_selected_names}, name=default_selected_names,
                           feathername={"fn": default_selected_metrics}, zvalue={"z": z_value}, times={"t": times},metricsvalue={"m_v": metrics_value}
                           ,selected_algorithms={"algorithms": default_algorithm}, lr_pred={"lr": lr_prediction})


@app.route('/line',methods=['GET','POST'])
def linecharttest():
    data = pd.read_csv('timeseries.csv')
    data_json = data.to_json(orient='records')
    metrics = ["CPI", "BW"]
    default_selected_names = "redis"
    a = json.loads(data_json)
    times_all = []
    metrics_value = []
    filter_data = []
    for i in a:
        if i["name"] == default_selected_names:
            times_all.append(i["time"])
            filter_data.append(i)

    for m in metrics:
        tmp = []
        for i in filter_data:
            tmp.append((i[m]))
        metrics_value.append(tmp)
    print (metrics_value)
    return render_template('linecharttest.html', times = {"t": times_all}, metrics = {"m": metrics}, metricsvalue={"m_v": metrics_value})


@app.route('/heat',methods=['GET','POST'])
def heatmaptest():
    data = pd.read_csv('timeseries.csv')
    data_json = data.to_json(orient='records')
    metrics = ["CPI", "BW", "L3_BW", "LLC"]
    #times = ["22:23", "22:24"]
    names = set(data["name"])
    default_selected_metrics = metrics
    default_selected_names = data["name"].tolist()[0]
    times = get_times(default_selected_names, data_json)
    z_value = get_z(default_selected_names, default_selected_metrics, data_json, times)

    if request.method == "POST":
        selected_metrics = request.form.getlist("metrics")
        selected_names = request.form.getlist("names")
        if selected_metrics!=None and selected_names!=None:
            print (selected_metrics)
            print(selected_names[0])
            z_value = get_z(selected_names[0], selected_metrics, data_json, times)
            print (z_value)
            return render_template("heatmaptest.html", metrics=metrics, selected_metrics = {"metrics": selected_metrics},
                                   names = names, selected_names = {"names": selected_names}, name=selected_names, feathername={"fn": selected_metrics}, zvalue={"z": z_value},times = {"t": times})
    print (times)
    return render_template('heatmaptest.html', metrics=metrics, names=names, selected_metrics = {"metrics": default_selected_metrics},
                           selected_names={"names": default_selected_names}, name=default_selected_names, feathername={"fn": default_selected_metrics}, zvalue={"z": z_value},times = {"t": times})

    #return render_template('heatmaptest.html', name=selected_name, feathername={"fn": s}, zvalue={"z": z_value})
if __name__ == '__main__':
    app.run()