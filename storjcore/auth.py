import email.utils
import time
from email.utils import parsedate_tz
from email.utils import mktime_tz
from datetime import datetime
from datetime import timedelta
from storjcore import sanitize


class AuthError(Exception):
    pass


def create_headers(btctxstore, recipient_address, sender_wif):
    """ Create authentication headers that can be used in a http query.

    Arguments:
        btctxstore: BtcTxStore instance used for signing.
        recipient_address: The bitcoin address of the recipient.
        sender_wif: Sender wallet used to sign the authentication message.

    Returns:
        {"Date": date, "Authorization": signature}

    Raises:
        storjcore.sanitize.ValidationError: if input is invalid
    """

    # sanitize input
    btctxstore = sanitize.is_btctxstore(btctxstore)
    recipient_address = sanitize.is_btcaddress(btctxstore, recipient_address)
    sender_wif = sanitize.is_btcwif(btctxstore, sender_wif)

    # create header date
    timeval = time.mktime(datetime.now().timetuple())
    date = email.utils.formatdate(timeval=timeval, localtime=True, usegmt=True)

    # create header signature
    msg = recipient_address + " " + date
    signature = btctxstore.sign_unicode(sender_wif, msg)
    return {"Date": date, "Authorization": signature}


def verify_headers(btctxstore, headers, timeout_sec,
                   sender_address, recipient_address):
    """ Verify authentication headers from http query.

    Arguments:
        btctxstore: BtcTxStore instance used to verify signature.
        headers: Authentication headers to be verified.
        timeout_sec: Timeout in seconds, where the date is valid.
        sender_address: Sender bitcoin address used for signing.
        recipient_address: The bitcoin address of the recipient.

    Returns:
        True if authentication headers are valid

    Raises:
        storjcore.auth.AuthError: if date or signature is invalid
        storjcore.sanitize.ValidationError: if input was invalid
    """

    # sanitize input
    btctxstore = sanitize.is_btctxstore(btctxstore)
    headers = sanitize.is_dict(headers)
    signature = sanitize.is_signature(headers.get("Authorization"))
    date = sanitize.is_header_date(headers.get("Date"))
    timeout_sec = sanitize.is_unsigned_int(timeout_sec)
    sender_address = sanitize.is_btcaddress(btctxstore, sender_address)
    recipient_address = sanitize.is_btcaddress(btctxstore, recipient_address)

    # verify date
    clientdate = datetime.fromtimestamp(mktime_tz(parsedate_tz(date)))
    timeout = timedelta(seconds=timeout_sec)
    delta = abs(datetime.now() - clientdate)
    if delta >= timeout:
        msg = "Invalid header date {0} >= {1}!".format(delta, timeout)
        raise AuthError(msg)

    # verify signature
    msg = recipient_address + " " + date
    if not btctxstore.verify_signature_unicode(sender_address, signature, msg):
        msg = "Invalid signature for auth addr {0}!".format(sender_address)
        raise AuthError(msg)
    return True
