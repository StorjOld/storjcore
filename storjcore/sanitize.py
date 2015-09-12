import base64
from btctxstore import BtcTxStore


class ValidationError(ValueError):
    pass


def is_any_string(s):
    if type(s) not in [type("string"), type(b"bytes"), type(u"unicode")]:
        raise ValidationError()
    return s


def is_unsigned_int(i):
    if (not isinstance(i, int)) or (not i >= 0):
        raise ValidationError()
    return i


def is_dict(d):
    if not isinstance(d, dict):
        raise ValidationError()
    return d


def is_signature(s):
    s = is_any_string(s)
    # FIXME convert to correct string type
    if len(base64.b64decode(s)) != 65:
        raise ValidationError()
    return s


def is_header_date(d):
    d = is_any_string(d)
    # FIXME implement
    return d


def is_btctxstore(btctxstore):
    if not isinstance(btctxstore, BtcTxStore):
        raise ValidationError()
    return btctxstore


def is_btcwif(btctxstore, wif):
    btctxstore = is_btctxstore(btctxstore)
    if not btctxstore.validate_key(wif):
        raise ValidationError()
    return wif


def is_btcaddress(btctxstore, address):
    """ TODO doc string """
    btctxstore = is_btctxstore(btctxstore)
    if not btctxstore.validate_address(address):
        raise ValidationError()
    return address
