import hashlib
import unittest
import tempfile
import storjcore


class TestEncryptedioSymmetric(unittest.TestCase):

    def test_roundtrip(self):
        encrypted_path = tempfile.mktemp()
        out_path = tempfile.mktemp()

        # symmetric_encrypt
        with open(__file__, 'rb') as fi, open(encrypted_path, 'wb') as fo:
            storjcore.encryptedio.symmetric_encrypt(fi, fo, b"test")

        # symmetric_decrypt
        with open(encrypted_path, 'rb') as fi, open(out_path, 'wb') as fo:
            storjcore.encryptedio.symmetric_decrypt(fi, fo, b"test")

        # check hashes
        with open(__file__, 'rb') as input_file:
            input_hash = hashlib.sha256(input_file.read()).hexdigest()
        with open(out_path, 'rb') as output_file:
            output_hash = hashlib.sha256(output_file.read()).hexdigest()
        self.assertEqual(input_hash, output_hash)

    @unittest.skip("TODO implement")
    def test_openssl_compatibility(self):
        pass
        # must be equivalent to
        # openssl aes-256-cbc -salt -in filename -out filename.enc
        # openssl aes-256-cbc -d -in filename.enc -out filename


if __name__ == '__main__':
    unittest.main()
