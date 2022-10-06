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

normal_incorrect_file = output_dir + 'bert/normal_wrong_idx.pkl'
abnormal_incorrect_file = output_dir + 'bert/abnormal_wrong_idx.pkl'

log_templates_file = output_dir + 'HDFS.log_templates.csv'
event_to_id = output_dir + 'hdfs_log_templates.json'

log_templates = pd.read_csv(log_templates_file)

with open(event_to_id, 'r') as f:
  event_to_id = json.load(f)

print(event_to_id)
print(log_templates.head())

log_templates['EventId'] = log_templates['EventId'].apply(lambda x : event_to_id[x]) 

log_templates = log_templates.sort_values(by=['EventId'])

print(log_templates.head())

log_templates_id_file = output_dir + 'HDFS.log_templates_id.csv'
log_templates.to_csv(log_templates_id_file, index=False)