# https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/MERRA2_DIURNAL/M2TUNXADG.5.12.4/1980/MERRA2_100.tavgU_2d_adg_Nx.198001.nc4.ascii?BCEMAN[0:23][226:281][85:190],time,lat[226:281],lon[85:190]


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
username = "USERNAME"
password = "PASSWORD"
session = SessionWithHeaderRedirection(username, password)

# ***********************
# Loop through Files
# ***********************


for single_date in daterange(start_date, end_date):
    YYYY = single_date.strftime("%Y")
    MM = single_date.strftime("%m")
    DD = single_date.strftime("%d")
    fpath1 = 'https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/MERRA2/M2I1NXASM.5.12.4/' + YYYY + '/' + MM + '/'
    fpath2 = 'MERRA2_400.inst1_2d_asm_Nx.' + YYYY + MM + DD + '.nc4.nc?'
    fpath3 = 'U2M[0:23][94:160][469:534],TROPT[0:23][94:160][469:534],TROPPB[0:23][94:160][469:534],' \
             'T2M[0:23][94:160][469:534],TQL[0:23][94:160][469:534],TOX[0:23][94:160][469:534],' \
             'PS[0:23][94:160][469:534],V50M[0:23][94:160][469:534],DISPH[0:23][94:160][469:534],' \
             'TO3[0:23][94:160][469:534],TS[0:23][94:160][469:534],T10M[0:23][94:160][469:534],' \
             'TROPPT[0:23][94:160][469:534],TQI[0:23][94:160][469:534],SLP[0:23][94:160][469:534],' \
             'TQV[0:23][94:160][469:534],V2M[0:23][94:160][469:534],TROPQ[0:23][94:160][469:534],' \
             'V10M[0:23][94:160][469:534],U50M[0:23][94:160][469:534],U10M[0:23][94:160][469:534],' \
             'QV2M[0:23][94:160][469:534],TROPPV[0:23][94:160][469:534],' \
             'QV10M[0:23][94:160][469:534],time,lat[94:160],lon[469:534]'

url = "https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/MERRA2_DIURNAL/M2TUNXADG.5.12.4/1980/MERRA2_100.tavgU_2d_adg_Nx.198001.nc4.ascii?BCEMAN[0:23][226:281][85:190],time,lat[226:281],lon[85:190]"
filename = "file1.nc4.nc"



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