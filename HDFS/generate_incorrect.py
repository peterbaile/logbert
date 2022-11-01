import pandas as pd
import json
from tqdm import tqdm
import os
import pickle
import numpy as np

output_dir = '../output/hdfs/'  # The output directory of parsing results
log_file   = "HDFS.log"
input_dir  = os.path.expanduser('./dataset/hdfs/')

log_templates_file = output_dir + log_file + "_templates.csv"
log_sequence_file = output_dir + "hdfs_sequence.csv"

normal_incorrect_file = output_dir + 'bert/normal_incorrect_idx_small.pkl'
abnormal_incorrect_file = output_dir + 'bert/abnormal_incorrect_idx_small.pkl'

test_normal_file = output_dir + 'test_normal_small'
test_abnormal_file = output_dir + 'test_abnormal_small'

normal_incorrect_idx = None
abnormal_incorrect_idx = None

with open(normal_incorrect_file, 'rb') as file:
  normal_incorrect_idx = pickle.load(file)
  print(len(normal_incorrect_idx))

with open(abnormal_incorrect_file, 'rb') as file:
  abnormal_incorrect_idx = pickle.load(file)
  print(len(abnormal_incorrect_idx)) 

normal = []
abnormal = []

with open(test_normal_file, "r") as f:
  for line in f.readlines():
    linea = line.split(' ')
    if len(linea) >= 10:
      normal.append(linea)

with open(test_abnormal_file, "r") as f:
  for line in f.readlines():
    linea = line.split(' ')
    if len(linea) >= 10:
      abnormal.append(linea)

normal_incorrect = np.array(normal, dtype=object)[normal_incorrect_idx]
abnormal_incorrect = np.array(abnormal, dtype=object)[abnormal_incorrect_idx]

with open(output_dir + "normal_incorrect_seq_small.pkl", 'wb') as f:
  pickle.dump(normal_incorrect, f)

with open(output_dir + "abnormal_incorrect_seq_small.pkl", 'wb') as f:
  pickle.dump(abnormal_incorrect, f)

normal_incorrect_idx.sort()
print(min(normal_incorrect_idx), max(normal_incorrect_idx))
print(np.histogram(normal_incorrect_idx, bins=[0, 1000, 2000]))

abnormal_incorrect_idx.sort()
print(min(abnormal_incorrect_idx), max(abnormal_incorrect_idx))
print(np.histogram(abnormal_incorrect_idx, bins=[0, 1000, 2000]))