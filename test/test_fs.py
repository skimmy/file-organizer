import os
import random
import unittest

from pynder.fs import hash_file

class FsTest(unittest.TestCase):
    def test_hash_file_md5(self):
        rand = random.randint(100000000, 999999999)
        file_path = f".fstest_{rand}"
        f = open(file_path, "w")
        f.write("Hello World!")
        f.close()
        expected = "ed076287532e86365e841e92bfc50d8c"
        actual = hash_file(file_path)
        self.assertEqual(expected, actual)
        os.remove(file_path)