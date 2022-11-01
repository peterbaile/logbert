import os
import pickle

output_dir = '../output/hdfs/'  # The output directory of parsing results
log_file   = "HDFS.log"
input_dir  = os.path.expanduser('./dataset/hdfs/')

result_file = output_dir + 'abnormal_incorrect_seq.pkl'

incorrect_seqs = None
seqs = []

with open(result_file, 'rb') as file:
  incorrect_seqs = pickle.load(file)
  # print(type(f))
  # print(type(f[0][0]))
  # print(f[:30])

for seq in incorrect_seqs:
  l = ' '.join(seq)
  # if '4 9 8 9 6' in l:
  for _ in range(50):
    seqs.append(l) 

with open('./test_abnormal_small', 'w') as f:
  f.writelines(seqs)

# seq_1 = '1 1 1 7 3 4 3 4 3 4 2 2 2 10 6 6 6 5 5 5\n'
# seq_2 = '1 7 3 4 1 3 4 1 3 4 2 2 2 10 6 6 6 5 5 5\n'
# seq_3 = '1 7 3 4 1 1 3 4 3 4 2 2 2 10 6 6 6 5 5 5\n'
# seq_4 = '1 7 1 1 3 4 3 4 3 4 2 2 2 10 6 6 6 5 5 5\n' # misclassified
# seq_5 = '7 1 1 1 3 4 3 4 3 4 2 2 2 10 6 6 6 5 5 5\n'
# seq_6 = '7 1 1 3 4 1 3 4 3 4 2 2 2 10 6 6 6 5 5 5\n'
# seq_7 = '7 1 1 3 4 3 4 1 3 4 2 2 2 10 6 6 6 5 5 5\n'
# seq_8 = '7 1 3 4 1 1 3 4 3 4 2 2 2 10 6 6 6 5 5 5\n'
# seq_9 = '7 1 3 4 1 3 4 1 3 4 2 2 2 10 6 6 6 5 5 5\n'

# seqs = []

# seqs_single = [seq_1, seq_2, seq_3, seq_4, seq_5, seq_6, seq_7, seq_8, seq_9]

# for seq in seqs_single:
#   for _ in range(1000):
#     seqs.append(seq) 

# with open('./test_normal_small', 'w') as f:
#   f.writelines(seqs)


# seq_1 = '7 1 1 1 3 4 3 4 2 2 2 3 4 9 8 9 6 6 6 5 5 5\n' # misclassified
# seq_2 = '7 1 1 1 3 4 3 4 2 2 2 3 4 6 6 6 5 5 5\n'

# seqs = []

# seqs_single = [seq_1, seq_2]

# for seq in seqs_single:
#   for _ in range(1000):
#     seqs.append(seq) 

# with open('./test_normal_small', 'w') as f:
#   f.writelines(seqs)