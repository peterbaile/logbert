import pandas as pd
import json
from tqdm import tqdm
import os
import pickle


import sys
sys.path.append("../")
sys.path.append("../../")

import os
dirname = os.path.dirname(__file__)

from bert_pytorch.dataset import LogDataset, WordVocab

output_dir = '../output/hdfs/'  # The output directory of parsing results
log_file   = "HDFS.log"
input_dir  = os.path.expanduser('./dataset/hdfs/')

log_templates_file = output_dir + log_file + "_templates.csv"
log_sequence_file = output_dir + "hdfs_sequence.csv"

result_file = output_dir + 'train'

count = 0

with open(result_file, 'rb') as file:
  f = pickle.load(file)
  print(len(f[0]))

# result_file = output_dir + 'test_abnormal'

# with open(result_file, "r") as f:
#   count = 0
#   for idx, line in tqdm(enumerate(f.readlines())):
#     linea = line.split(' ')
#     if len(linea) >= 10:
#       count += 1
  
#   print(count)