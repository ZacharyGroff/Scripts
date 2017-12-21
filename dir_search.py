'''
This script was created to search directories
   for all files modified in a day.
Two files (filelog.txt & found.txt) are created
    in the same directory that holds this file.
'''

import os
import datetime
import sys

f = open('filelog.txt', 'w+')
print('What directory would you like to search?')
root = str(input())

# ensure path is valid
if not os.path.exists(root):
    print('{} is not a valid directory'.format(root))
    sys.exit()

# search directories starting at user given root
#   and write paths to file_list
for subdir, dirs, files in os.walk(root):
    for file in files:
        f.write(str(os.path.join(subdir, file)) + '\n')

file_list = open('filelog.txt').read().splitlines()
current_date = str(datetime.date.today())
found_log = open('found.txt', 'w+')
files_found = 0

# check if each file in file_list has been modified today
#   and write it to found_log
for path in file_list:
    try:
        access_date = str(datetime.date.fromtimestamp(
            os.path.getmtime(path)))
        
        if current_date == access_date:
            found_log.write(path + '\naccessed:\t' 
                    + access_date + '\n')
            files_found += 1
    
    except (PermissionError, FileNotFoundError):
        continue

print('{} files found modified today in {}'.format(files_found, root))
