import unittest
from btctxstore import BtcTxStore
from storjcore import auth


class TestConfig(unittest.TestCase):

    def test_it(self):
        btctxstore = BtcTxStore()
        sender_wif = btctxstore.create_key()
        timeout = 2
        sender = btctxstore.get_address(sender_wif)
        recipient = btctxstore.get_address(btctxstore.create_key())
        headers = auth.create_headers(btctxstore, recipient, sender_wif)
        self.assertTrue(auth.validate_headers(btctxstore, headers, timeout,
                                              sender, recipient))



if __name__ == '__main__':
    unittest.main()

