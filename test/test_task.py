# Copyright 2023 Michele Schimd

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==========================================================================
import shutil
import sqlite3
import unittest

from testing_util import random_file_name, create_testing_dir, fill_testing_db
import pynder.task as task

class TaskTest(unittest.TestCase):
    
    def setUp(self) -> None:
        self.dir_name = random_file_name()
        self.db = sqlite3.connect(":memory:")
        create_testing_dir(root_dir=self.dir_name)
        fill_testing_db(self.db)
        
    def tearDown(self) -> None:
        shutil.rmtree(self.dir_name)
    
    def test_add_repo(self):
        path = "/mnt/external"
        description = "External drive"
        actual = task.add_repo(self.db, path, description)
        self.assertIsNotNone(
            actual,
            msg="Repository insertion should have been succeeded."
        )
        result = self.db.execute("SELECT * FROM repository WHERE id=?;", (actual, ))
        records = result.fetchall()
        self.assertIn(
            (actual, description, path),
            records,
            msg="Tuple not found after SELECT",
        )

