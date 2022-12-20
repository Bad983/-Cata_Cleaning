import os
import re
import glob
import pandas as pd
from natsort import natsorted

# PARAMETRI GLOBALI
root_folder = 'data'

# DATI
data_folder_name_originale = 'Originale'
filename_originale = 'ORIG_DIVINA_COMMEDIA_INFERNO_*.txt'

data_folder_name_traduzione = 'Traduzione'
filenamepath_traduzione_it_1 = 'TRAD_6_DIVINA_COMMEDIA_INFERNO_IT_*.txt'

DATA_PATH_ORIGINAL = os.path.abspath(os.path.join(root_folder, data_folder_name_originale))
orig_filenamepath = os.path.abspath(os.path.join(DATA_PATH_ORIGINAL, filename_originale))

DATA_PATH_TRANSLATE = os.path.abspath(os.path.join(root_folder, data_folder_name_traduzione))
trad_filenamepath_it_1 = os.path.abspath(os.path.join(DATA_PATH_TRANSLATE, filenamepath_traduzione_it_1))

data_folder_out = 'data_out'
DATA_PATH_OUT = os.path.abspath(os.path.join(data_folder_out, 'divina_commedia_inferno_'))


def transform_roman_numeral_to_number(roman_numeral):
    roman_char_dict = {'i': 1, 'v': 5, 'x': 10, 'l': 50, 'c': 100, 'd': 500, 'm': 1000}
    res = 0
    for i in range(0, len(roman_numeral)):
        if i == 0 or roman_char_dict[roman_numeral[i]] <= roman_char_dict[roman_numeral[i - 1]]:
            res += roman_char_dict[roman_numeral[i]]
        else:
            res += roman_char_dict[roman_numeral[i]] - 2 * roman_char_dict[roman_numeral[i - 1]]
    return res


for filename in glob.glob(orig_filenamepath):
    number = ((filename.split('/')[-1]).split('.')[0]).split('_')[-1]

    if not number.isdigit():
        number_output = transform_roman_numeral_to_number(number)
        os.rename(filename, os.path.abspath(
            os.path.join(DATA_PATH_ORIGINAL, 'ORIG_DIVINA_COMMEDIA_INFERNO_' + str(number_output) + '.txt')))

for file_orig, file_trad_1 in zip(natsorted(glob.glob(orig_filenamepath)),
                                  natsorted(glob.glob(trad_filenamepath_it_1))):

    df_orig = pd.read_csv(file_orig, header=None, sep='\\n', names=['Original'], engine='python')
    df_trad_1 = pd.read_csv(file_trad_1, header=None, sep='\\n', names=['Translate_IT_1'], engine='python')

    df_orig = pd.DataFrame(re.split('[.!;]', re.sub('-', '', ' '.join(df_orig['Original']))),
                           columns=['Original']).dropna()

    traduzione_1 = re.sub('-', '', ' '.join(df_trad_1['Translate_IT_1']))
    traduzione_1 = re.sub('\([^)]*\)', '', traduzione_1)
    traduzione_1 = re.split('[.!]', traduzione_1)

    df_trad_1 = pd.DataFrame(traduzione_1, columns=['Translate_IT_1']).dropna()

    number = ((file_orig.split('/')[-1]).split('.')[0]).split('_')[-1]
    df = df_orig.join(df_trad_1).dropna()

    df.to_csv(DATA_PATH_OUT + str(number) + '.csv', index=False)



