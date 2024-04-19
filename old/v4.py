import requests
from datetime import timedelta, date

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

start_date = date(2016, 1, 1)
end_date = date(2019, 7, 31)

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
username = "kmotia"
password = "Fuckyounasa1!"
session = SessionWithHeaderRedirection(username, password)

# ***********************
# Loop through Files
# ***********************

url = "https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/MERRA2_DIURNAL/M2TUNXADG.5.12.4/1980/MERRA2_100.tavgU_2d_adg_Nx.198001.nc4.ascii?BCEMAN[0:23][226:281][85:190],time,lat[226:281],lon[85:190]"
# print(url)



# extract the filename from the url to be used when saving the file
filename = 'file2.txt'
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