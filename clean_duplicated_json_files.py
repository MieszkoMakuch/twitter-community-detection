import json
from os import listdir
from os.path import isfile, join

'''
Used to clean corrupted json files that have more than one json inside. 
This script cuts the file leaving only the first line
'''

USER_DIR = 'data/users'

onlyfiles = [f for f in listdir(USER_DIR) if isfile(join(USER_DIR, f))]
print("size: " + str(len(onlyfiles)))
counter = 0
for i, file in enumerate(onlyfiles):
    if file == '.DS_Store':
        continue
    file_path = join(USER_DIR, file)
    try:
        user = json.loads(open(file_path, encoding="utf-8").read())
    except ValueError as error:
        counter += 1
        print("fixing error in file: " + file + ", counter=" + str(counter) + " of " + str(i))
        with open(file_path, 'r', encoding="utf-8") as fin:
            data = fin.read().splitlines(True)
        with open(file_path, 'w', encoding="utf-8") as fout:
            fout.writelines(data[0])
