import hashlib
import partialhash


# FIXME remove reward wif (will use micropayment channels instead)


def generate_response(btctxstore, data, challenge):
    """ Generates the response for a requested audit.

    Arguments:
        btctxstore: BtcTxStore instance used generate the reward wif.
        data: File path or file like object.
        challenge: challenge bytes

    Returns:
        { "response": sha256sum, "reward_wif": bitcoin_wif }
    """
    # TODO validate input

    # get reward secret sha256sum(challenge + data)
    reward_secret = partialhash.compute(data, seed=challenge)

    # generate reward wif from reward secret
    reward_wif = btctxstore.create_key(master_secret=reward_secret)

    # get response (second hash to prevent infering of the reward secret)
    response = hashlib.sha256(reward_secret).digest()

    return { "response": response, "reward_wif": reward_wif }



def verify_response(data, challenge, response):
    """ Generates the response for a requested audit.

    Arguments:
        data: File path or file like object.
        challenge: challenge bytes
        response: The audit response to verify.

    Returns:
        True if response is correct.

    """
    # TODO validate input

    # get reward secret sha256sum(challenge + data)
    reward_secret = partialhash.compute(data, seed=challenge)

    # get response sha256sum(reward secret)
    generated_response = hashlib.sha256(reward_secret).digest()

    return response == generate_response

