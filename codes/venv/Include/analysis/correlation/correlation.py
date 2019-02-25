import numpy as np
import pandas as pd
np.set_printoptions(suppress=True)
def prepare_subset():
    dataset = pd.read_csv("subset.csv")
    subset = dataset.drop(['benchmark_id','cluster'], axis=1)
    return subset

data = prepare_subset().values
result = np.corrcoef(data,rowvar=0)
df=pd.DataFrame(result)
df.to_csv(r"correlation.csv")
