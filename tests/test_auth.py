import time
import base64
import unittest
import storjcore
from btctxstore import BtcTxStore


class TestAuth(unittest.TestCase):

    def setUp(self):
        self.btctxstore = BtcTxStore()
        self.sender_wif = self.btctxstore.create_key()
        self.sender = self.btctxstore.get_address(self.sender_wif)
        recipient_wif = self.btctxstore.create_key()
        self.recipient = self.btctxstore.get_address(recipient_wif)

    def test_self_validates(self):
        headers = storjcore.auth.create_headers(self.btctxstore,
                                                self.recipient,
                                                self.sender_wif)

        self.assertTrue(storjcore.auth.verify_headers(self.btctxstore,
                                                      headers,
                                                      5, self.sender,
                                                      self.recipient))

    def test_invalid_signature(self):
        def callback():
            headers = storjcore.auth.create_headers(self.btctxstore,
                                                    self.recipient,
                                                    self.sender_wif)
            headers["Authorization"] = base64.b64encode(65 * b"x")
            storjcore.auth.verify_headers(self.btctxstore, headers,
                                          5, self.sender, self.recipient)
        self.assertRaises(storjcore.auth.AuthError, callback)

    def test_timeout_to_old(self):
        def callback():
            headers = storjcore.auth.create_headers(self.btctxstore,
                                                    self.recipient,
                                                    self.sender_wif)
            time.sleep(5)
            storjcore.auth.verify_headers(self.btctxstore, headers,
                                          5, self.sender, self.recipient)
        self.assertRaises(storjcore.auth.AuthError, callback)

    @unittest.skip("TODO implement")
    def test_timeout_to_young(self):
        pass  # FIXME how to test this?


if __name__ == '__main__':
    unittest.main()
