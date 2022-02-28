import numpy as np
from numpy import linalg as LA
import pandas as pd
import math

from tqdm import tqdm

from sentence_transformers import util

npy = np.load("data/embedded_act_pass.npy")
active = npy[:,0]
passive = npy[:,1]
difference = npy[:,6]

# Calculates the mean of the difference vectors of the active and passive sentences
mean_difference_vector = np.reshape(np.mean(difference, axis = 0), (1,768))
# To each passive vector, we add the mean differnce vector
passive_plus_mdv = np.add(passive, mean_difference_vector)

# This function finds euclidean distance between active and passive_plus_mdv.
# Then we find how close the ith element is to the smallest euclidean distance, 
# ie how close is active[i] to passive_plus_mdv[i]?
# The method uses np.argsort to return the indices of the sorted list
def comparing_active_to_passive_plus_mdv():
    lst = []
    for i in tqdm(range(10000)):
        sublst = []
        for j in range(10000):
            sublst.append(LA.norm(active[j,:] - passive_plus_mdv[i,:]))
        argsorted = np.argsort(np.array(sublst))
        lst.append(np.where(argsorted ==  i))
    return np.array(lst).flatten()

result = comparing_active_to_passive_plus_mdv()

print(np.mean(result))
print(np.count_nonzero(result))