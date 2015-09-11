import hashlib
import unittest
import tempfile
import storjcore


class TestEncryptedio(unittest.TestCase):

    def test_roundtrip(self):
        encrypted_path = tempfile.mktemp()
        output_path = tempfile.mktemp()

        # encrypt
        with open(__file__, 'rb') as in_file, open(encrypted_path, 'wb') as\
                out_file:
            storjcore.encryptedio.encrypt(in_file, out_file, b"test")

        # decrypt
        with open(encrypted_path, 'rb') as in_file, open(output_path, 'wb') as\
                out_file:
            storjcore.encryptedio.decrypt(in_file, out_file, b"test")

        # check hashes
        with open(__file__, 'rb') as input_file:
            input_hash = hashlib.sha256(input_file.read()).hexdigest()
        with open(output_path, 'rb') as output_file:
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
