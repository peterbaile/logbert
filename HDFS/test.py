import matplotlib.pyplot as plt
import numpy as np
from scipy.special import logsumexp
import pandas as pd

# create data
x = np.array([[1, 2], [3, 4], [5, 6]])

y = np.array([1, 3, 5])

print(x/y[:, None])

# print('-------stupid way-----------')

# x = np.array([[-2.96913* -23.32164, -2.96913* -23.19959], [-3.43382*-23.32164, -3.43382*-23.19959]])
# A = np.array([[0.79034887, 0.20965113], [0.66824331, 0.33175669]])
# r = x * A

# r /= np.sum(r)

# print(r)

# [0.64523, 0.00601]