logs = []

block_id = 'blk_-597126776337351848'

with open('./dataset/hdfs/HDFS.log', 'r') as f:
  for line in f.readlines():
    if block_id in line:
      logs.append(line)

with open(f'./dataset/hdfs/{block_id}.log', 'w') as f:
  f.writelines(logs)