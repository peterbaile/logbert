with open('./docker_log.txt', 'r') as f:
  lines = f.readlines()


data_node_count = 0
blk_count = 0
for line in lines:
  if 'blk_1073742713_1889' in line:
    print(line)
  # if 'datanode         |' in line:
  #   data_node_count += 1
  #   if 'blk_' in line:
  #     blk_count += 1
  #     if 'Scheduling ' in line:
  #       print('!!!')
      

print(f'{blk_count}/ {data_node_count}')