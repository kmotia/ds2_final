import re
import os

folder_name = 'BCEMAN_files'
# Find urls for data files and put them in a list
with open(f'links/{folder_name}.txt', 'r') as file:
    url_list = []
    line_number = 0
    for line in file:
        if line_number > 0:
            url_list.append(line.strip())  # remove any leading or trailing whitespace
        line_number+=1


extracted_nums = []
match_pattern = r'Nx\.(\d{6})'
for url in url_list:
    # print(url)
    match = re.findall(match_pattern, url)
    print((match[0]))

    folder_name = folder_name
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    filename = f'{folder_name}_files/{folder_name[:6]}_{str(match[0])}.txt'
    print(filename)