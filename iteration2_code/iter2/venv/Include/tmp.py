import json
import pandas as pd
import re

data = pd.read_csv('timeseries.csv')
a = data.to_json(orient='records')
filtered_data = []
selected_name = "redis"
metrics = ["CPI", "BW", "L3_BW", "LLC"]
z_value = []
a = json.loads(a)
times = ["22:23", "22:24"]

for i in a:
    if i["name"] == selected_name and i["time"] in times:
        filtered_data.append(i)
        times.append(i["time"])

print (filtered_data)
for m in metrics:
    tmp = []
    for i in filtered_data:
        if m in i.keys():
            tmp.append(i[m])
        #tmp1.append({"metric": m, "data": tmp})
    z_value.append(tmp)

# s = json.loads(re.sub('\'', '\"', json.dumps(filtered_data)))
#s = json.loads(re.sub('\'', '\"', json.dumps(data_clean)))
#print(s)
print (z_value)