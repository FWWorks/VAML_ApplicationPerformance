from sklearn import preprocessing
import numpy as np
import pandas as pd

def prepare_subset():
    dataset = pd.read_csv("subset.csv")
    subset = dataset.drop(['benchmark_id','cluster'], axis=1)
    return subset

dataset = prepare_subset().values
min_max_scaler = preprocessing.MinMaxScaler()
X_minMax = min_max_scaler.fit_transform(dataset)
result = np.around(X_minMax, decimals=2)
df=pd.DataFrame(result)
df.to_csv(r"minMax.csv")