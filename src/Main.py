# -*- coding: utf-8 -*-
"""Main module: Calls the parser and writer functionality implemented in CsvTools. This is a 2 step process.

1. The three csv files are opened and parsed in order. user_dict is continuously populated during this process with the
   the data contained in these csv files.
2. The contents of the user dictionary is passed to the write_csv function. This data is dumped into a csv file in a
   nicely formatted way. 
   
"""
from CsvTools import parse_csv, write_csv

resource_dir = "resources/"
output_filename = "Formatted_Password_Log_Data.csv"
csv_file_names = ["Text28_log.csv", "Imagept28_log.csv", "Blankpt28_log.csv"]
user_dict = {}


# Populate user_dict with user and login data from all the csv files
for file_name in csv_file_names:
    csv_path = resource_dir + file_name
    parse_csv(user_dict, csv_path)


# Write a single csv file with this data
write_csv(resource_dir + output_filename, user_dict)
