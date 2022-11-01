#Importing initial packages
import os
import sys
import subprocess
import warnings

#Implement pip as subprocess to install required dependencies.
print('Checking for dependencies \n')
subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                      'numpy'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                      'pandas'])

print('Finished dependencies check! \n')

#Importing rest of packages
import numpy as np
import pandas as pd


warnings.filterwarnings('ignore')

print('*****'*10)
print('Data Extractor for output files of Center for Genomic Epidemiology.')
print('Author: Christopher W. Smith')
print('Date of Creation: 11/01/2022')
print('Version Number: 1 \n')

#Set folder for file path
path = input("What is the folder path?: " )
path = print(path)
file_list = []

print('\n' + '*****'*10)
file_type = input("What file types do you want to use, .txt, .tsv, etc...: " )

for file in os.listdir(path):
    if file.endswith(file_type):
        file_list.append(file)

#Opening first dataframe
df = pd.read_csv(file_list[0], sep = '\t')

#Selecting column to sort data from.
print('')
print('This is the columns from the {} file found.'.format(file_type))
print('Which column would you like to select for sorting?')

column_list = list(df.columns)
for i in np.arange(0, len(df.columns)):
    print('{}: {}'.format(i, column_list[i]))

number_column_selected = input('\n Please type number of column selected: ')
column_selected = column_list[int(number_column_selected)]

#Importing first dataset to form dataframe
file_list_length = len(file_list)
new_df = pd.DataFrame(columns=list(df[column_selected].unique()), index=range(file_list_length))
new_df.loc[0] = 'yes'
print(new_df.head())
print('\n')

#Separating new files into dictionary
file_dict = {}

#Setting file names for dictionary keys
file_names = []
for i in np.arange(0, len(file_list)):
    file_names.append(file_list[i].replace('{}'.format(file_type), ''))

#Setting dictionary up
for i in np.arange(1, len(file_list)):
    temp_df = pd.read_csv(file_list[i], sep='\t')
    file_dict[file_names[i]] = list(temp_df[column_selected].unique())

#Imputing data to new_df to create table
new_df_columns = list(new_df.columns)

for i in np.arange(0, len(file_dict)):
    key = list(file_dict.keys())[i]
    print('Imputing {} data!'.format(key))
    data = file_dict[key]
    for j in np.arange(0, len(data)):
        
        if data[j] in new_df_columns:
            new_df[data[j]][i+1] = 'yes'
        
        else:
            new_df_columns.append(data[j]) #Appends unknown column label
            new_df[data[j]] = 'yes'
            new_df[data[j]] = np.nan
            new_df[data[j]][i+1] = 'yes'

#Converting null to no and converting row index names
new_df = new_df.replace(np.nan, 'no')
new_df.index = file_names

print('\n Updated data frame. \n')
print('*****'*10 + '\n')
print(new_df)
print('\n Please save data with .csv in ending. \n If new path is required, please include path as well.')

output_file_name = input('\n Please type file name: ')
new_df.to_csv(output_file_name)
print('File saved as {}! \n Goodbye!'.format(output_file_name))