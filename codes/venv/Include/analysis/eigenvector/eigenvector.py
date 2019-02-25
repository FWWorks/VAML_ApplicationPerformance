from sklearn.decomposition import PCA
import numpy as np
import pandas as pd

def prepare_subset():
    dataset = pd.read_csv("subset.csv")
    subset = dataset.drop(['benchmark_id','cluster'], axis=1)
    return subset


def pca(dataset):
    pca = PCA(n_components=2)
    new = pca.fit_transform(dataset)
    return pca.components_, new
        #ratio = pca.explained_variance_ratio_
        #print (pca.explained_variance_)
        #print (dataset.columns.tolist())

def get_most_important_components(lst, dataset):
    pca = lst[0]
    attrs = dataset.columns.tolist()
    result = {}
    i = 0
    if len(attrs) != len(pca):
        print("pca error")
        return 0
    for attr in attrs:
        result[attr] = pca[i]
        i = i + 1
    #print (sorted(result.items(), key=lambda d: d[1], reverse=True))
    firsttwo = sorted(result.items(), key=lambda d: d[1], reverse=True)[:2]
    re = []
    for f in firsttwo:
        re.append(f[0])
    return re

dataset = prepare_subset()
a = pca(dataset)[0]
projection = pca(dataset)[1]
print (a)
#print (get_most_important_components(a, dataset))
#print (projection)
#df=pd.DataFrame(projection)
#df.to_csv(r"projection.csv")