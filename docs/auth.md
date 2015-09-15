
# Storj authentication protocol

This document describes how one storj node authenticates itself to another.


## Authentication keys

Each node has a [bitcoin ECDSA Secp256k1](https://en.bitcoin.it/wiki/Private_key) key pair.

 * The [bitcoin address](https://en.bitcoin.it/wiki/Address) is use as the nodes ID.
 * The public/private keys are use to verify/sign messages.


## Authentication protocol


### 1. The sender signs the authentication message.

Authentication message components:

 * Recipient [bitcoin address](https://en.bitcoin.it/wiki/Address)
 * Timestamp ([Http header date/time rfc2616](http://tools.ietf.org/html/rfc2616#section-3.3))

The authentication message signed by the sender is in the following format: `<recipient address> <timestamp>`

Signing must be compatible with the bitcoind reference implementation .

    bitcoind signmessage <sender address> <authentication message>


### 2. The sender sends information to the recipient.

The following information is sent:

 * Base64 encoded signature
 * Authentication message timestamp
 * Sender address
 * Additional data

The authentication message timestamp must be identical to the one used when signing, as the recipient uses this to reconstruct the authentication message for signature verification.


### 3. Recipient validates 

*Timestamp validation*

The recipient checks if the provided authentication message timestamp is within an acceptable delay to the current time.
What delay is acceptable is at the discretion of the recipient (recommended is a valid range of +-15 seconds).
If the provided timestamp is not within the acceptable range authentication fails.


*Signature validation*

The recipient reconstructs the authentication message signed by the sender and verifies that it is correct.

Signature verification must be compatible with the bitcoind reference implementation .

    bitcoind verifymessage <sender address> <signature> <authentication message>  


## HTTP compatibility

The timestamp and signature format is chosen such that it can be easily inserted into the HTTP Date and Authorization headers.


## Reference implementation

See /storjcore/auth.py for a reference implementation.


## Possible improvements

Include the communication data in the authentication message. This will provide additional validation of the communication data.




