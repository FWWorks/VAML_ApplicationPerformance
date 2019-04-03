from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

import numpy as np
import pandas as pd

def get_pca_data(data, header): # data:dataframe
    data = data[header]
    X_std = StandardScaler().fit_transform(data.values)

    pca = PCA(n_components=5)
    eigenvector = pca.fit_transform(X_std)
    #print (pca.explained_variance_)
    ratio = pca.explained_variance_ratio_
    ratio = [(str(round(i*100,2)) + "%") for i in ratio]
    return eigenvector, ratio

'''
header = ["BW","MEM_BW","switch","cpu","io","memory","network"]
data = pd.read_csv("pmd.csv")
a = get_pca_data(data, header)
print (a[0])
print ("=====")
print (a[1])
'''