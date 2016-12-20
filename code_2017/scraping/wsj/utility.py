import argparse
import logging
import requests
from time import sleep

from selenium import webdriver


def log(message, level = 'info'):

    """

    log

    Message : String -> Level : String -> Void

    Simple logging utility function


    ex. log("Helloworld")


    """

    l = logging
    l.basicConfig(filename='history.log',level=logging.DEBUG,format='%(asctime)s %(message)s' )

    {"info": l.info, "debug" : l.debug, "warning" : l.warning}[level](message)


def u_and_p():

    """
    u_and_p 

    -> (Username: String, Password: String)


    Selects -u and -p parameter from the command line and returns them as strings

    ex. -u beiberfan123 -p password1234

    """

    parser = argparse.ArgumentParser(description='Begin collecting wsj articles')
    parser.add_argument('-u','--user', required=True)
    parser.add_argument('-p','--password', required=True)
    args = vars(parser.parse_args())
    return args['user'], args['password']
    
def login(username,password):

    d = webdriver.PhantomJS()

    login_url = 'https://id.wsj.com/access/pages/wsj/us/signin.html?url=http%3A%2F%2Fwww.wsj.com&mg=id-wsj'

    d.get(login_url)

    u_input = d.find_element_by_xpath('//*[@id="username"]')
    u_input.clear()
    u_input.send_keys(username)

    p_input = d.find_element_by_xpath('//*[@id="password"]')
    p_input.clear()
    p_input.send_keys(password)


    d.find_element_by_xpath('//*[@id="js-login-submit-button"]').click()

    s = requests.Session()

    for c in d.get_cookies():

        s.cookies.set(c['name'], c['value'])

    d.close()

    return s

def make_request(url, headers, request, error, session = False, return_json = False, refresh_session = None):

    """

    make_request

    url : String ->  #  Url to be visited
    headers: Dict<String: String> ->  # Request Headers
    request: Float ->  # Time out Delay
    session: Dict<String:String> ->  # Session Object
    return_json:Boolean ->  # Will it return a json object?
    refresh_ession: Session Object ->  # Should it refresh the session

    Return : Json | String | None


    This function helps make a request. It is handy because it will try to make the request again
    if the function times out.

    ex. make_request('google.com', '{'header1':'value1'}', 1800 seconds, '{'cookie':'value'}', False))

    """

    get_function = session.get if session else requests.get

    try:
        go_to_sleep("About to make request {}".format(url), request)

        if return_json:

            return get_function(url, headers = headers, timeout = 200).json()

        return get_function(url, headers = headers, timeout = 200).text

    except Exception as e:
        
        go_to_sleep(e, error)

        if refresh_session:
            session = refresh_session()

    try:
        go_to_sleep("Again lets try {}".format(url), request)   

        if return_json:
            return get_function(url, headers = headers, timeout = 200).json()
            
        return get_function(url, headers = headers, timeout = 200).text

    except Exception as e:
        log ("Given up on link due to :{}:".format(e))
        return None

def go_to_sleep(msg, time_in_sec, verbose = True):

    """

    go_to_sleep

    Message : String ->  # Message to be logged
    Time : Int ->  # Sleep duration
    Verbose: Boolean ->  # Should print or not
    Void 


    """
    
    time_str = "Sleeping for {sec}"
    if time_in_sec > 30:
        segment = time_in_sec / 3
        for stage in range(3):
            log("Asleep:  {stage}/2".format(stage = stage))
            sleep(segment)
    else:
        "Sleeping for {sec}".format(sec=time_in_sec)
        sleep(time_in_sec)