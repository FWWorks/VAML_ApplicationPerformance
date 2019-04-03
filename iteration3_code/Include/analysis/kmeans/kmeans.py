from sklearn.cluster import KMeans
import pandas as pd

def kmeans(dataset):
    y_pred = KMeans(n_clusters=13, random_state=9).fit_predict(dataset)
    return y_pred

def prepare_subset():
    dataset = pd.read_csv("projection.csv")
    return dataset

df = prepare_subset()
cluster = kmeans(df)

d = []
for i in range(0, len(df)):
    tmp = []
    tmp.append(df.iloc[i][0])
    tmp.append(df.iloc[i][1])
    tmp.append(cluster[i])
    d.append(tmp)

df = pd.DataFrame(d)
df.to_csv(r"projection.csv")