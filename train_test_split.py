#import functions as f

import os
import re
import numpy as np
from sklearn.model_selection import train_test_split

#
main_path = 'data/tales/'
files = os.listdir(main_path)
files

#
files_with_max_count = {title[:-5]: title[-5:-4] for title in files}
files_unique = [key + str(np.random.randint(1, int(value)+1)) + '.txt' for key, value in files_with_max_count.items()]

#
sample_size = 800

files_ids = list(range(len(files_unique)))
files_ids_sample = np.random.choice(files_ids, sample_size, replace=False)

#
train_ids, test_ids = train_test_split(files_ids_sample, test_size=0.2, random_state=42)

#
train = ''
test = ''
eot_token = '<| end of text |>'

for i in train_ids:
    #tale = f.read_txt(main_path + files_unique[i])
    tale = read_txt(main_path + files_unique[i])
    tale = re.sub(' +', ' ', tale.replace('\n',' '))
    train += tale + ' ' + eot_token + ' '

for i in test_ids:
    #tale = f.read_txt(main_path + files_unique[i])
    tale = read_txt(main_path + files_unique[i])
    tale = re.sub(' +', ' ', tale.replace('\n',' '))
    test += tale + ' ' + eot_token

#
exclude_words = [eot_token, '']
print('train')
#f.text_summary(train, exclude_words)
text_summary(train, exclude_words)
print('\ntest')
#f.text_summary(test, exclude_words)
text_summary(test, exclude_words)

#
#f.save_txt(train, 'data/train.txt')
save_txt(train, 'data/train.txt')
#f.save_txt(test, 'data/test.txt')
save_txt(test, 'data/test.txt')