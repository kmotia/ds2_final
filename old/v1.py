from http.cookiejar import CookieJar
import http.cookiejar as cookielib

from urllib.parse import urlencode
 
import urllib.request as urllib2

 
# The user credentials that will be used to authenticate access to the data
 
username = "kmotia "
password = "Fuckyounasa1!"
  
 
# The url of the file we wish to retrieve
 
url = "https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/MERRA2_DIURNAL/M2TUNXADG.5.12.4/1980/MERRA2_100.tavgU_2d_adg_Nx.198001.nc4.ascii?BCEMAN[0:23][226:281][85:190],time,lat[226:281],lon[85:190]"
 
 
# Create a password manager to deal with the 401 reponse that is returned from
# Earthdata Login
 
password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
password_manager.add_password(None, "https://urs.earthdata.nasa.gov", username, password)
 
 
# Create a cookie jar for storing cookies. This is used to store and return
# the session cookie given to use by the data server (otherwise it will just
# keep sending us back to Earthdata Login to authenticate).  Ideally, we
# should use a file based cookie jar to preserve cookies between runs. This
# will make it much more efficient.
 
cookie_jar = CookieJar()
  
 
# Install all the handlers.
 
opener = urllib2.build_opener(
    urllib2.HTTPBasicAuthHandler(password_manager),
    #urllib2.HTTPHandler(debuglevel=1),    # Uncomment these two lines to see
    #urllib2.HTTPSHandler(debuglevel=1),   # details of the requests/responses
    urllib2.HTTPCookieProcessor(cookie_jar))
urllib2.install_opener(opener)
 
 
# Create and submit the request. There are a wide range of exceptions that
# can be thrown here, including HTTPError and URLError. These should be
# caught and handled.
 
request = urllib2.Request(url)
response = urllib2.urlopen(request)
 
 
# Print out the result (not a good idea with binary data!)
 
body = response.read()
