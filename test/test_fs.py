import os
import random
import unittest

from testing_util import random_file_name
from pynder.fs import hash_file

class FsTest(unittest.TestCase):
    def test_hash_file_md5(self):
        file_path = random_file_name()
        f = open(file_path, "w")
        f.write("Hello World!")
        f.close()
        expected = "ed076287532e86365e841e92bfc50d8c"
        actual = hash_file(file_path)
        self.assertEqual(expected, actual)
        os.remove(file_path)