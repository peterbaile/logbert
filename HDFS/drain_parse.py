import sys
sys.path.append('../')

from logparser import Drain
import os
import pandas as pd


input_dir  = os.path.expanduser('./dataset/hdfs/')
output_dir = '../output/hdfs/'  # The output directory of parsing results
log_file   = "docker_log.log"  # The input log file name

def parser(input_dir, output_dir, log_file, log_format):
  regex = [
      r"(?<=blk_)[-\d]+", # block_id
      r'\d+\.\d+\.\d+\.\d+',  # IP
      r"(/[-\w]+)+",  # file path
      # r'(?<=[^A-Za-z0-9])(\-?\+?\d+)(?=[^A-Za-z0-9])|[0-9]+$',  # Numbers
  ]
  # the hyper parameter is set according to http://jmzhu.logpai.com/pub/pjhe_icws2017.pdf
  st = 0.5  # Similarity threshold
  depth = 5  # Depth of all leaf nodes


  parser = Drain.LogParser(log_format, indir=input_dir, outdir=output_dir, depth=depth, st=st, rex=regex, keep_para=False)
  parser.parse(log_file)

if __name__ == "__main__":
  # 1. parse HDFS log
  log_format = '<Machine> \| <Date> <Time> <Level> <Content>'  # HDFS log format
  # parser(input_dir, input_dir, log_file, log_format)

  # read CSV and sort in descending order of occurrences
  df = pd.read_csv(f'./dataset/hdfs/{log_file}_templates.csv')
  df = df.sort_values(by='Occurrences', ascending=False)
  df.to_csv(f'./dataset/hdfs/{log_file}_templates_sorted.csv', index=False)
  # print(df.head(10))