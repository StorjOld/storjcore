import datetime
import email.utils
import time


def create_headers(btctxstore, remote_address, authentication_wif):
    timeval = time.mktime(datetime.datetime.now().timetuple())
    date = email.utils.formatdate(timeval=timeval, localtime=True, usegmt=True)
    msg = remote_address + " " + date
    signature = btctxstore.sign_unicode(authentication_wif, msg)
    return {"Date": date, "Authorization": signature}
