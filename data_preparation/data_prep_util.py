import csv
import pandas as pd
import numpy as np
#import json
#from threading import Thread
#from threading import Lock
#import time
#from Levenshtein import distance
#import random
import unicodedata
import re
import data_prep_consts

def read_csv_file(path):
  """
  read_in data as data frame
  """
  return pd.read_csv(path)


def save_txt_to_file(filename, text_content, mode = 'a'):
  """
  comment
  """
  #global BLOCKING_INPUT_DIR
  f = open(data_prep_consts.BLOCKING_INPUT_DIR + filename, mode, encoding = 'utf-8')
  f.write(text_content)
  f.close()
  

def prepare_columns_scm(dataframe):
  #global ISO_CODES
  dataframe.rename(columns = {'c.iso2':'Country', 's.name':'Company'}, inplace = True)
  country_query = ''
  
  for iso_code in data_prep_consts.ISO_CODES:
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


def normalize_unicode(value):
    return unicodedata.normalize('NFKD', value)


def change_umlaut(text):
    umlaute = {u"ö":"oe", u"ä":"ae", u"ü":"ue", u"Ö":"OE", u"Ä":"AE", u"Ü":"UE", u"ß":"ss", u'ö':'oe', u'ä':'ae', u'Ü':'UE', u'Ü':'UE', u'ü':'ue', u'ü':'ue', u'Ö':'OE', u'Ä':'AE'}
    for key, value in umlaute.items():
        text = text.replace(key, value)
    return text


#detect entries with high ord
threshold = 0.5
current_idx = 0

def detect_high_ord(text):
  global threshold
  count_ord = 0
  for ch in text:
      if ord(ch) > 1000:
          count_ord += 1
  
  return round(len(text)*threshold) >= count_ord


"""#overwriting already translated chinese names
def replace_chinese_translation(parsed_company, df):
  global current_idx
  country = df['Country'][current_idx]
  company = df['Company'][current_idx]
  current_idx += 1
  
  if country != 'CN':
      return parsed_company
  
  if detect_high_ord(company):
      return company
  
  return parsed_company"""

#overwriting already translated chinese names
def replace_chinese_translation(parsed_company, df, column):
  global current_idx
  country = df['Country'][current_idx]
  company = df['Company'][current_idx]
  city = df['city'][current_idx]
  current_idx += 1
  
  if country != 'CN':
    return parsed_company
  
  if column == 'company' and detect_high_ord(company):
    return company
  
  if column == 'city' and detect_high_ord(city):
    return city
    
  return parsed_company


def clear_company_name(entry):
  parsed_entry = entry.lower()

  for rm_word in data_prep_consts.REMOVAL_WORDS:
    parsed_entry = parsed_entry.replace(rm_word, '')

  for rm_sep in data_prep_consts.REMOVAL_SEPARATORS:
    parsed_entry = parsed_entry.replace(rm_sep, ' ')
  
  parsed_entry = parsed_entry.replace('  ', ' ')

  return parsed_entry.strip()


def find_brackets_in_string(text):
  open_brackets = 0
  bracket_value = ''
  SEPARATOR = ', '
  
  for character in text:
      
      if character == ')':
          open_brackets -= 1
                  
      if open_brackets > 0:
          bracket_value += character
          
      if character == '(':
          
          if (len(bracket_value) != 0) and (open_brackets == 0):
              bracket_value += SEPARATOR
              
          open_brackets += 1
          
  if SEPARATOR in bracket_value:
      sep_idx = bracket_value.index(SEPARATOR)
      if bracket_value[sep_idx + len(SEPARATOR):] == bracket_value[:sep_idx]:
          return bracket_value[sep_idx + len(SEPARATOR):].replace('"','')
        
  return bracket_value.replace('"','')


#drops unnecessary location column content
def clear_location_column(location_value):
  
    for rm_word in data_prep_consts.REMOVAL_WORDS_LOCATION_SCM:
        location_value = location_value.replace(rm_word, '')
        
    return location_value

#
def company_category(company, country):
    if country == 'DE':
      for key, value in data_prep_consts.COMPANY_CATEGORIES['DE'].items():
          if key in company:
              return value
            
    for key, value in data_prep_consts.COMPANY_CATEGORIES['INTERNATIONAL'].items():
        if key in company:
            return value
    
    if country == 'DE':
      for suffix in data_prep_consts.REMOVE_COMPANY_SUFFIXES['DE']:
          if re.match('.* ' + suffix + '$', company.replace('"','')):
              return data_prep_consts.COMPANY_CATEGORIES['SUFFIX'][suffix]
    
    for suffix in data_prep_consts.REMOVE_COMPANY_SUFFIXES['INTERNATIONAL']:
          if re.match('.* ' + suffix + '$', company.replace('"','')):
              return data_prep_consts.COMPANY_CATEGORIES['SUFFIX'][suffix]

#drops unnecessary content from company name
def clear_comp_name_column(comp_value):
    for rm_word in data_prep_consts.REMOVAL_WORDS_COMPANY_NAME_SCM:
        comp_value = comp_value.replace('(' + rm_word + ')', '').replace('(' + rm_word, '').replace(rm_word + ')', '')
        
    return comp_value


#remove location content from company name
def clear_company_content(df):
    for index,row in df.iterrows():
        cities = row['Location'].split(", ")
        
        for city in cities:
            df['Parsed_Company'][index] = df['Parsed_Company'][index].replace(('(' + city + ')'), '').replace(('(' + city), '').replace((city + ')'), '')
    
        space = ' '
        for i in range(13, 1, -1):
            df['Parsed_Company'][index] = df['Parsed_Company'][index].replace((space*i), ' ')


def remove_suffixes(parsed_comp):
    remove_suffixes = [' ag', ' se', ' eg', ' ev', ' e v', ' ek', ' e k', ' ohg', ' ug', ' gmbh']
    for suffix in remove_suffixes:
        parsed_comp = re.sub(suffix + '$', '', parsed_comp)
    return parsed_comp


def replace_float_city(city):
    if type(city) != str:
        city = ''
    return city