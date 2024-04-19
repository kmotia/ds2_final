# # Find urls for data files and put them in a list
# with open('aerosol_data_links.txt', 'r') as file:
#     url_list = []
#     line_number = 0
#     for line in file:
#         if line_number > 0:
#             url_list.append(line.strip())  # remove any leading or trailing whitespace
#         line_number+=1
# print(url_list[0])
# print(url_list[1])
# print(url_list[-1])
# # print(len(url_list))

import re

# Find urls for data files and put them in a list
with open('aerosol_data_links.txt', 'r') as file:
    url_list = []
    line_number = 0
    for line in file:
        if line_number > 0:
            url_list.append(line.strip())  # remove any leading or trailing whitespace
        line_number+=1


# match_pattern = r'Nx\.(\d{6})'
# for url in url_list:
#     print(url)
#     matches = re.findall(match_pattern, url)
#     extracted_numbers = [int(match) for match in matches]
#     print(extracted_numbers)

extracted_nums = []
match_pattern = r'Nx\.(\d{6})'
for url in url_list:
    # print(url)
    matches = re.findall(match_pattern, url)
    print((matches[0]))
#     extracted_nums.append(matches)
# print(extracted_nums)