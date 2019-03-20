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
