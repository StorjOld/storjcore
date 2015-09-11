import time
import unittest
from btctxstore import BtcTxStore
from storjcore import auth


class TestConfig(unittest.TestCase):

    def setUp(self):
        self.btctxstore = BtcTxStore()
        self.sender_wif = self.btctxstore.create_key()
        self.sender = self.btctxstore.get_address(self.sender_wif)
        self.recipient = self.btctxstore.get_address(self.btctxstore.create_key())

    def test_self_validates(self):
        headers = auth.create_headers(self.btctxstore, self.recipient,
                                      self.sender_wif)
        self.assertTrue(auth.validate_headers(self.btctxstore, headers,
                                              2, self.sender, self.recipient))

    def test_timeout_to_old(self):
        def callback():
            headers = auth.create_headers(self.btctxstore, self.recipient,
                                          self.sender_wif)
            time.sleep(2)
            self.assertTrue(auth.validate_headers(self.btctxstore, headers,
                                                  2, self.sender,
                                                  self.recipient))
            self.assertRaises(callback, auth.AuthError)

    @unittest.skip("")
    def test_timeout_to_young(self):
        pass


if __name__ == '__main__':
    unittest.main()

