import email.utils
import time
from email.utils import parsedate_tz
from email.utils import mktime_tz
from datetime import datetime
from datetime import timedelta
from storjcore import validate


class AuthenticationError(Exception):
    pass


def create_headers(btctxstore, recipient_address, authentication_wif):

    # validate input
    btctxstore = validate.is_btctxstore(btctxstore)
    recipient_address = validate.is_btcaddress(recipient_address)
    authentication_wif = validate.is_btcwif(authentication_wif)

    # create header date and signature
    timeval = time.mktime(datetime.now().timetuple())
    date = email.utils.formatdate(timeval=timeval, localtime=True, usegmt=True)
    msg = recipient_address + " " + date
    signature = btctxstore.sign_unicode(authentication_wif, msg)
    return {"Date": date, "Authorization": signature}


def validate_headers(btctxstore, headers, timeout_sec,
                     sender_address, recipient_address):
    # validate input
    btctxstore = validate.is_btctxstore(btctxstore)
    headers = validate.is_dict(headers)
    signature = validate.is_signature(headers.get("Authorization"))
    date = validate.is_rfc7231_date(headers.get("Date"))
    timeout_sec = validate.is_unsigned_int(timeout_sec)
    sender_address = validate.is_btcaddress(sender_address)
    recipient_address = validate.is_btcaddress(recipient_address)

    # verify date
    clientdate = datetime.fromtimestamp(mktime_tz(parsedate_tz(date)))
    timeout = timedelta(seconds=timeout_sec)
    delta = abs(datetime.now() - clientdate)
    if delta >= timeout:
        msg = "Invalid header date {0} >= {1}!".format(delta, timeout)
        raise AuthenticationError(msg)

    # verify signature
    msg = recipient_address + " " + date
    if not btctxstore.verify_signature_unicode(sender_address, signature, msg):
        msg = "Invalid signature for auth addr {0}!".format(sender_address)
        raise AuthenticationError(msg)
    return True
