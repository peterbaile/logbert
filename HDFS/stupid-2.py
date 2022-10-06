import pandas as pd
import json
from tqdm import tqdm
import os
import pickle

output_dir = '../output/hdfs/'  # The output directory of parsing results
log_file   = "HDFS.log"
input_dir  = os.path.expanduser('./dataset/hdfs/')

log_templates_file = output_dir + log_file + "_templates.csv"
log_sequence_file = output_dir + "hdfs_sequence.csv"

result_file = output_dir + 'abnormal_incorrect_seq.pkl'

with open(result_file, 'rb') as file:
  f = pickle.load(file)
  print(f[:30])

# result_file = output_dir + 'test_abnormal'

# with open(result_file, "r") as f:
#   count = 0
#   for idx, line in tqdm(enumerate(f.readlines())):
#     linea = line.split(' ')
#     if len(linea) >= 10:
#       count += 1
  
#   print(count)