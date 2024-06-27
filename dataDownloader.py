import requests
import re
import os
import constants as c

# This script was modified from a similar file found on NASA GES DISC.


# ***********************
# overriding requests.Session.rebuild_auth to maintain headers when redirected
# ***********************
class SessionWithHeaderRedirection(requests.Session):
    AUTH_HOST = 'urs.earthdata.nasa.gov'

    def __init__(self, username, password):
        super().__init__()
        self.auth = (username, password)

    # Overrides from the library to keep headers when redirected to or from the NASA auth host.
    def rebuild_auth(self, prepared_request, response):
        headers = prepared_request.headers
        url = prepared_request.url
        if 'Authorization' in headers:
            original_parsed = requests.utils.urlparse(response.request.url)
            redirect_parsed = requests.utils.urlparse(url)
            if (original_parsed.hostname != redirect_parsed.hostname) and \
               redirect_parsed.hostname != self.AUTH_HOST and \
               original_parsed.hostname != self.AUTH_HOST:
                del headers['Authorization']
        return


# create session with the user credentials that will be used to authenticate access to the data
username = c.username
password = c.password
session = SessionWithHeaderRedirection(username, password)

# ***********************
# Loop through Files
# ***********************

# Specify pollutant name --> BCEMAN, OCEMAN, SO2EMAN, SO4EMAN --> SO2EMAN is for SO2
data_name = 'SO2EMAN'           

# Find urls for data files and put them in a list
with open(f'links/{data_name}_links.txt', 'r') as file:
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

    folder_name = f'{data_name}_files'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    filename = f'{folder_name}/{data_name}_{str(match[0])}.txt'
    print(filename)

    try:
        # submit the request using the session
        response = session.get(url, stream=True)
        print(response.status_code)

        # raise an exception in case of http errors
        response.raise_for_status()

        # save the file
        with open(filename, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                fd.write(chunk)

    except requests.exceptions.HTTPError as e:
        # handle any errors here
        print(e)




