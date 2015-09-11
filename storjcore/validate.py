

class ValidationError(Exception):
    pass


def is_unsigned_int(i):
    if (not isinstance(i, int)) or (not i >= 0):
        raise ValidationError()
    return i


def is_dict(d):
    if not isinstance(d, dict):
        raise ValidationError()
    return d


def is_signature(s):
    # FIXME implement
    return s


def is_rfc7231_date(d):
    # FIXME implement
    return d


def is_btcaddress(address):
    # FIXME implement
    return address


def is_btcwif(wif):
    # FIXME implement
    return wif


def is_btctxstore(btctxstore):
    # FIXME implement
    return btctxstore
