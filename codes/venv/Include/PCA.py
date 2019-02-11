# importing computation data manipulation and plotting modules
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

def prepare_subset():
    dataset = pd.read_csv("VAML_dataset.csv", error_bad_lines=False)
    subset = dataset.drop_duplicates(subset="DISTSIM_BENCH.benchmark_id", keep='first', inplace=False)
    subset = subset[~subset['DISTSIM_BENCH.benchmark_id'].str.contains(';')]
    subset = subset[~(subset['date'].map(lambda d: d.split('/')[0])).isin(['8'])]
    subset.to_csv("subset.csv",index=False,sep=',')

def load_dataset():
    subset = pd.read_csv("subset.csv", error_bad_lines=False)
    cols = [i for i in subset.columns if i not in ['benchmark_id']]
    subset_no_name = subset[cols]
    subset_no_name = subset_no_name.fillna(0)

    subset_std = (subset_no_name - np.mean(subset_no_name, axis=0)) / np.std(subset_no_name, axis=0)
    subset_std = np.nan_to_num(subset_std)
    cov_matrix = np.cov(subset_std, rowvar=False)
    #print (cov_matrix)
    cov_matrix = np.nan_to_num(cov_matrix)
    #print(cov_matrix)
    eigenvalues, eigenvectors, = np.linalg.eig(cov_matrix)
    eigen_pairs = [(eigenvalues[index], eigenvectors[:,index]) for index in range(len(eigenvalues))]

    # Get eigenvalues and eigenvectors
    eigvalues_sort = [eigen_pairs[index][0] for index in range(len(eigenvalues))]
    eigvectors_sort = [eigen_pairs[index][1] for index in range(len(eigenvalues))]
    topTwo = np.array(eigvectors_sort[0:2]).transpose()
    #print (topTwo)
    Proj_data_2D = np.dot(subset_std, topTwo)
    print (len(Proj_data_2D))
    negative = plt.scatter(Proj_data_2D[:, 0], Proj_data_2D[:, 1])
    plt.title('First PCA')
    plt.ylabel('host_L2_BW')

    # x-axis
    plt.xlabel('host_disk_io')

    # plot
    plt.show()


load_dataset()