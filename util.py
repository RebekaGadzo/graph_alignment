# UTIL before moving script from data_prepocessing
def save_txt_to_file(filename, text_content, mode = 'a'):
  """
  comment
  """
  global BLOCKING_INPUT_DIR
  f = open(BLOCKING_INPUT_DIR + filename, mode, encoding = 'utf-8')
  f.write(text_content)
  f.close()

def filter_companies_by_country(dataframe, iso_code):
  """
  comment
  """
  df = dataframe[dataframe.Country == iso_code]
  return df

def form_colval_pairs(values1, values2, matching):
  """
  comment
  """
  pair1 = ''
  pair2 = ''
  
  for column in values1:
    if len(pair1) > 0:
      pair1 += ' '
    pair1 += 'COL ' + column[0] + ' VAL ' + column[1]
    
  for column in values2:
    if len(pair2) > 0:
      pair2 += ' '
    pair2 += 'COL ' + column[0] + ' VAL ' + column[1]

  return pair1 + '\t' + pair2 + '\t' + str(matching)

def compare_company_names(scm_company, coypu_company):

  """
  droping out unnecessery buzzwords from company names
  comparing prefix of company names -> if comparisson successeds compute levenstein distance and checks if it's within defined thresshold
  """

  scm_company_parsed = scm_company.lower().replace('gmbh', '').replace('& co.', '').replace('(', '').replace(')', '').replace('llc', '').replace('ltd', '').replace(' ag', '').replace(' kg', '')
  coypu_company_parsed = coypu_company.lower().replace('gmbh', '').replace('& co.', '').replace('(', '').replace(')', '').replace('llc', '').replace('ltd', '').replace(' ag', '').replace(' kg', '')

  compare_index = min(5, len(scm_company_parsed) // 2, len(coypu_company_parsed) // 2)

  if scm_company_parsed[0:compare_index] != coypu_company_parsed[0:compare_index]:
    return 0

  value_distance = distance(scm_company_parsed, coypu_company_parsed)

  threshold_distance = max(len(scm_company_parsed), len(coypu_company_parsed)) * THRESHOLD

  if value_distance > threshold_distance:
    return 0

  return 1

def shuffle_txtfile_lines(filename):
  """
  comment
  """
  lines = open(BLOCKING_INPUT_DIR + filename, encoding = 'utf-8').readlines()
  random.shuffle(lines)
  open(BLOCKING_INPUT_DIR + filename, 'w', encoding = 'utf-8').writelines(lines)

def read_csv_file(path):
  """
  read_in data as data frame
  """
  return pd.read_csv(path)

def prepare_columns_scm(dataframe):
  dataframe.rename(columns = {'c.iso2':'Country', 's.name':'Company'}, inplace = True)
  country_query = ''
  
  for iso_code in ISO_CODES:
    if len(country_query) > 0:
      country_query += ' or '
    country_query += '(Country == "' + iso_code + '")'

  dataframe_sub = dataframe.query(country_query)
  dataframe_sub.reset_index(inplace = True)
  # del dataframe_sub['index']

  return dataframe_sub

def prepare_columns_coypu(dataframe):
  dataframe.rename(columns = {'country':'Country', 'name':'Company'}, inplace = True)
  # del dataframe[dataframe. columns[0]]

  return dataframe

def split_data(filename):
    #split data to train, test, val
    lines = open(BLOCKING_INPUT_DIR + filename, encoding = 'utf-8').readlines()
    
    train_treshold = round(len(lines) * 0.8)
    test_treshold = round(len(lines) * 0.9)
    
    open(BLOCKING_INPUT_DIR + filename[:-4] + '_train.txt', 'w', encoding = 'utf-8').writelines(lines[:train_treshold])
    open(BLOCKING_INPUT_DIR + filename[:-4] + '_test.txt', 'w', encoding = 'utf-8').writelines(lines[train_treshold:test_treshold])
    open(BLOCKING_INPUT_DIR + filename[:-4] + '_val.txt', 'w', encoding = 'utf-8').writelines(lines[test_treshold:])
    
  #izbaciti nerelevantne metode
    