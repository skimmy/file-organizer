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
import os
import sqlite3
import unittest

import testing_util as tu
import pynder.db as db

class DbTest(unittest.TestCase):

    def setUp(self):
        self.db_name = tu.random_file_name(ext="sqlite")
        self.db = sqlite3.connect(self.db_name)

    def fillDb(self):
        tu.fill_testing_db(self.db)

    def tearDown(self):
        self.db.close()
        os.remove(self.db_name)

    def test_has_schema_empty_db(self):
        self.assertFalse(db.has_schema(
            self.db.cursor()),
            msg="Detected schema where should not be present"
        )

    def test_has_schema_ok(self):
        self.db.execute("CREATE TABLE IF NOT EXISTS file(md5, path)")
        self.db.commit()
        self.assertTrue(db.has_schema(
            self.db.cursor()),
            msg="Undetected schema when should be present"
        )

    def test_has_table_empty(self):
        self.assertFalse(
            db.has_table(self.db, 'file'),
            msg="Table 'file' found and supposedly empty DB"
        )

    def test_has_table_ok(self):
        self.db.execute("CREATE TABLE IF NOT EXISTS file(md5, path)")
        self.db.commit()
        self.assertTrue(
            db.has_table(self.db, 'file'),
            msg="Table 'file' not found after insertion"
        )

    def test_has_table_wrong_name(self):
        self.db.execute("CREATE TABLE IF NOT EXISTS file(md5, path)")
        self.db.commit()
        self.assertFalse(
            db.has_table(self.db, 'author'),
            msg="Table 'author' found but 'file' table was inserted"
        )

    def test_file_exists_found(self):
        self.fillDb()
        md5, _ = tu.TEST_FILE_RECORDS[0]
        self.assertTrue(
            db.file_exists(self.db, md5),
            msg="Didn't found expected row in 'file' table",
        )

    def test_file_exists_not_found(self):
        self.fillDb()
        md5 = "aabbccddeeff6767"
        self.assertFalse(
            db.file_exists(self.db, md5),
            msg="Found unexpected row in 'file' table",
        )

    def test_repository_by_path_found(self):
        self.fillDb()
        repo = (1, "Temp", "/tmp")
        actual = db.repository_by_path(self.db, repo[2])
        expected = [repo]
        self.assertEquals(
            len(expected),
            len(actual),
            msg=f"Length of returned list ({len(actual)}) doesn't match what expected ({len(expected)}).",
        )
        self.assertIn(
            repo,
            actual,
            msg="Didn't found the expected repository tuple in result."
        )

    def test_repository_by_path_not_found(self):
        self.fillDb()
        repo = (11, "TMP", "/temp")
        actual = db.repository_by_path(self.db, repo[2])
        expected = []
        self.assertEquals(
            len(expected),
            len(actual),
            msg=f"Length of returned list ({len(actual)}) doesn't match what expected ({len(expected)}).",
        )
        self.assertNotIn(
            repo,
            actual,
            msg="Found a tuple not expected to be in the result."
        )

    def test_repository_by_path_multiple(self):
        self.fillDb()
        repo = (11, "TMP", "/tmp")
        self.db.execute(
            "INSERT INTO repository VALUES(?, ?, ?);",
            repo
        )
        actual = db.repository_by_path(self.db, repo[2])
        expected = [repo, tu.TEST_REPO_RECORDS[0]]
        self.assertEquals(
            len(expected),
            len(actual),
            msg=f"Length of returned list ({len(actual)}) doesn't match what expected ({len(expected)}).",
        )
        for r in expected:
            self.assertIn(
                r,
                actual,
                msg="Didn't found the expected repository tuple in result."
            )
        

    def test_create_schema_ok(self):
        path = tu.random_file_name()
        new_db = sqlite3.connect(path)
        db.create_schema(new_db)
        created = sqlite3.connect(path)
        for table in tu.ALL_TABLES:
            self.assertTrue(
                db.has_table(created, table),
                msg=f"Table {table} not found after create schema."
            )
        created.close()
        os.remove(path)

    def test_add_file_ok(self):
        self.fillDb()
        md5 = "abcd1234abcd1234"
        path = "/home/user/foo.txt"
        db.add_file(self.db, md5, path)
        result = self.db.execute(f"SELECT * FROM file WHERE md5='{md5}';")
        first = result.fetchone()
        self.assertIsNotNone(
            first,
            msg="Fail to fetch any file record with md5 just inserted."
        )
        self.assertEqual(
            first[1],
            path,
            msg=f"Inserted path is {path}, but query gives {first[1]}."
        )

    def test_add_file_with_repo_ok(self):
        self.fillDb()
        md5 = "abcd1234abcd1234"
        path = "/tmp/foo.txt"
        db.add_file(self.db, md5, None, repository=1, path=path)
        result = self.db.execute(f"SELECT * FROM file WHERE md5='{md5}';")
        first = result.fetchone()
        self.assertIsNotNone(
            first,
            msg="Fail to fetch any file record with md5 just inserted."
        )
        result = self.db.execute(
            f"SELECT * FROM repository_file WHERE id_file='{md5}';")
        results = result.fetchall()
        self.assertIn(
            (1, md5, path),
            results,
            msg="Entry not found in 'repository_file' table."
        )

    def test_add_file_existing(self):
        self.fillDb()
        md5, publication = tu.TEST_FILE_RECORDS[0]
        rowcount = db.add_file(self.db, md5, publication)
        self.assertEqual(
            rowcount,
            0,
            msg="Not 0 rows have been created after adding existing tuple."
        )

    def test_insert_repo_ok(self):
        self.fillDb()
        path = "C:\\USER\\BOOK\\"
        description = "A good repo"
        id_repo = db.add_repository(self.db, path, description)
        print("----->", id_repo)
        result = self.db.execute(f"SELECT * FROM repository;")
        all = result.fetchall()
        self.assertIn(
            path,
            [r[2] for r in all],
            msg="Inserted path not found."
        )
        self.assertIn(
            description,
            [r[1] for r in all],
            msg="Inserted description not found."
        )
        result = self.db.execute(
            f"SELECT * FROM repository WHERE id={id_repo};")
        records = result.fetchall()
        self.assertEqual(
            len(records),
            1,
            msg="The number of returned records is not 1."
        )
        self.assertEquals(
            records[0],
            (id_repo, description, path),
            msg="Retrieved record doesn't match expected values."
        )

    def test_list_of_files_ok(self):
        self.fillDb()
        expected = [record[0] for record in tu.TEST_FILE_RECORDS]
        obtained = db.list_of_files(self.db)
        self.assertEqual(
            set(expected),
            set(obtained),
            msg="Set of obtained and returned md5's are different."
        )

    def test_list_of_repositories_ok(self):
        self.fillDb()
        expected = [(int(t[0]), t[1], t[2]) for t in tu.TEST_REPO_RECORDS]
        obtained = db.list_of_repository(self.db)
        self.assertEqual(
            set(expected),
            set(obtained),
            msg="Set of obtained and returned repositories differ."
        )
