import pandas as pd
import json
from Levenshtein import distance
import random
import data_prep_consts

class ColValueBuilder:
  def __init__(self):
    self.columns = []

  def add_column(self, df_column, custom_name):
    self.columns.append({'column_name': df_column, 'custom_name': custom_name})
    return self

  def build(self, data_frame):
    aggregated_value = ''

    for row in data_frame.iterrows():
      aggregated_value += self.transform_row(row) + '\n'
    
    return aggregated_value
    
  def transform_row(self, row):
    row_value = ''
    
    for col in self.columns:
      row_value +=  'COL ' + col['custom_name'] + ' VAL ' + str(row[col['column_name']]) + ' '
    
    return row_value

def save_txt_to_file(filename, text_content, mode = 'a'):
  """
  comment
  """
  #global BLOCKING_INPUT_DIR
  f = open(filename, mode, encoding = 'utf-8')
  f.write(text_content)
  f.close()

def form_colval_pairs(values1, values2, matching):
  """
  comment
  """
  pair1 = ''
  pair2 = ''
  
  for column in values1:
    if len(pair1) > 0:
      pair1 += ' '
    pair1 += 'COL ' + column[0] + ' VAL ' + str(column[1])
    
  for column in values2:
    if len(pair2) > 0:
      pair2 += ' '
    pair2 += 'COL ' + column[0] + ' VAL ' + str(column[1])

  return pair1 + '\t' + pair2 + '\t' + str(matching)

def compare_company_names(scm_company_parsed, coypu_company_parsed, threshold):

  """
  droping out unnecessery buzzwords from company names
  comparing prefix of company names -> if comparisson successeds compute levenstein distance and checks if it's within defined thresshold
  """
  
  if scm_company_parsed == None or coypu_company_parsed == None:
    return 0

  if type(scm_company_parsed) != str or type(coypu_company_parsed) != str:
    print(scm_company_parsed, coypu_company_parsed)

  compare_index = min(5, len(scm_company_parsed) // 2, len(coypu_company_parsed) // 2)

  if scm_company_parsed[0:compare_index] != coypu_company_parsed[0:compare_index]:
    return 0

  value_distance = distance(scm_company_parsed, coypu_company_parsed)

  threshold_distance = max(len(scm_company_parsed), len(coypu_company_parsed)) * threshold

  if value_distance > threshold_distance:
    return 0

  return 1

def shuffle_txtfile_lines(filename):
  """
  comment
  """
  lines = open(filename, encoding = 'utf-8').readlines()
  random.shuffle(lines)
  open(filename, 'w', encoding = 'utf-8').writelines(lines)

def read_csv_file(path):
  """
  read_in data as data frame
  """
  return pd.read_csv(path)

def split_data(filename):
    #split data to train, test, val
    lines = open(filename, encoding = 'utf-8').readlines()
    
    train_treshold = round(len(lines) * 0.8)
    test_treshold = round(len(lines) * 0.9)
    
    open(filename[:-4] + '_train.txt', 'w', encoding = 'utf-8').writelines(lines[:train_treshold])
    open(filename[:-4] + '_test.txt', 'w', encoding = 'utf-8').writelines(lines[train_treshold:test_treshold])
    open(filename[:-4] + '_val.txt', 'w', encoding = 'utf-8').writelines(lines[test_treshold:])