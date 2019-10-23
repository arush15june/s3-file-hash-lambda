import unittest

from memory_profiler import profile

import crypter
SMALL_FILE_PATH = 'tests/small_file.txt'
LARGE_FILE_PATH = 'tests/large_file.txt'

class CrypterTest(unittest.TestCase):

    @profile
    def test_small_file_sha_256(self):
        file_data = crypter.read_file_data(SMALL_FILE_PATH)
        hashed = crypter.hash_sha_256(file_data)
        print(hashed)

if __name__ == '__main__':
    unittest.main()
