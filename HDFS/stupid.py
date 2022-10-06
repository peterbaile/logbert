import pandas as pd
import json
from tqdm import tqdm
import os

output_dir = '../output/hdfs/'  # The output directory of parsing results
log_file   = "HDFS.log"
input_dir  = os.path.expanduser('./dataset/hdfs/')

log_templates_file = output_dir + log_file + "_templates.csv"
log_sequence_file = output_dir + "hdfs_sequence.csv"

blk_label_file = os.path.join(input_dir, "anomaly_label.csv")
blk_df = pd.read_csv(blk_label_file)
blk_df = blk_df[blk_df['Label'] == 'Anomaly']
correct_ids = set(blk_df['BlockId'].tolist())
print(len(correct_ids))

anomaly_ids = []

with open(log_templates_file, 'r') as f:
  for line in f:
    s = line.lower().split(',')
    if 'error' in s[1]:
      anomaly_ids.append(s[0])

log_temp = pd.read_csv(log_templates_file)
log_temp.sort_values(by = ["Occurrences"], ascending=False, inplace=True)
log_temp_dict = {event: idx+1 for idx , event in enumerate(list(log_temp["EventId"])) }

anomaly_idx = [log_temp_dict[id] for id in anomaly_ids]

anomaly_blocks = []

log_seq = pd.read_csv(log_sequence_file)
for index, row in tqdm(log_seq.iterrows()):
  x = json.loads(row['EventSequence'])
  for idx in anomaly_idx:
    if idx in x:
      anomaly_blocks.append(row['BlockId'])
      break

blk_label_file = os.path.join(input_dir, "anomaly_label.csv")
blk_df = pd.read_csv(blk_label_file)

diff = set(anomaly_blocks).difference(correct_ids)
print(len(diff))
print(diff)

for index, row in log_seq.iterrows():
  if row['BlockId'] in diff:
    print(row['EventSequence'])

print(anomaly_blocks[:3])

print(len(anomaly_blocks))


