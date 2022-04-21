# -*- coding: utf-8 -*-
"""
Get noise class from noise wav file name.
For example, "__5V2Njkf5M.wav" --> ['Sampler', 'Music', 'Speech']
"""
import os
import csv
import re
from colorama import Fore, Back, Style

#Input noise wav files
noise_path = r'D:\Work\Dataset\speech\DNS-Challenge\datasets\noise'
#Defining audio wav file name and noise class string
unbalanced_train_segments_path = r'unbalanced_train_segments.csv'
#Mapping between noise class string and noise type, for example "/m/0k4j" vs "car" 
mid_to_display_name_path = r'class_labels_indices.csv'
#Output label files
output_file = r'files_labels.md'


with open(unbalanced_train_segments_path, 'r') as f:
    unbalanced_train_segments =[row for row in csv.reader(f)]

with open(mid_to_display_name_path, 'r') as f:
    mid_to_display_name =[row for row in csv.reader(f)]
#tranform to dict
mid_to_display_name_dict = {}
for item in mid_to_display_name:
  #item = item[0]
  #__, key, value = re.split(r'\t', item)
  __, key, value = item
  mid_to_display_name_dict[key] = value    

audiofiles = [name for name in os.listdir(noise_path)
              if name.endswith('.wav')]

files_labels = {}
for file_name in audiofiles:
  raw_file_name = file_name[:-4]
  
  if r'Freesound' in raw_file_name:
    idx = raw_file_name.find(r'Freesound')
    label_names = [raw_file_name[:idx-1]]       
  else:
    label = 'unknown'
    for row in unbalanced_train_segments:
      if raw_file_name in row:
          label = row[3:]
          break
  
    label_names = []
    for item in label:
      #remove the ' ' and " in the string  
      item = item.replace(' ', '')
      item = item.replace('"', '')
      try:
        label_name = mid_to_display_name_dict[item]  
      except KeyError:
        print(Fore.RED +"KeyError: label match fail:", item)
        label_name = r'unknow label'
      label_names.append(label_name)
  files_labels[raw_file_name] = label_names
  print(Fore.WHITE+raw_file_name, label_names)
  
      
with open(output_file, 'wt') as f:
  for item in files_labels.keys(): 
     f.write(item + ' ' + str(files_labels[item])+'\n') 
  f.close()
