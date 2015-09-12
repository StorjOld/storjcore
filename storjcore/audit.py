import partialhash


def generate_response(data, challange):
    """ Generates the response for a requested audit.

    Arguments:
        data: File path or file like object. 
        challange: challange bytes

    Returns:
        sha256sum(challange + data)
        
    """
    # TODO validate input
    return partialhash.compute(data, seed=challange)


def verify_response(data, challange, response):
    """ Generates the response for a requested audit.

    Arguments:
        data: File path or file like object. 
        challange: challange bytes
        response: The audit response to verify.

    Returns:
        True if response is correct.
        
    """
    # TODO validate input
    return response == generate(data, challange)

