import os
import sqlite3
import unittest

from testing_util import random_file_name
import pynder.db as db

ALL_TABLES = [
    "publication",
    "file",
    "author",
    "topic",
    "repository",
    "author_pub",
    "topic_pub",
    "repository_file"
]

TEST_FILE_RECORDS = [
    ("12345678abcdabcd", None),
    ("9876543210112233", 1),
    ("aabbccddeeff0000", 2)
]

TEST_REPO_RECORDS = [
    (1, "Temp", "/tmp"),
    (2, "Main", "/home/users/books")
]

class DbTest(unittest.TestCase):
    
    def setUp(self):
        self.db_name = random_file_name(ext="sqlite")
        self.db = sqlite3.connect(self.db_name)
    
    def fillDb(self):
        db.create_schema(self.db)
        for file_record in TEST_FILE_RECORDS:
            self.db.execute(
                "INSERT INTO file VALUES(?, ?);",
                file_record
            )
        for repo_record in TEST_REPO_RECORDS:
            self.db.execute(
                "INSERT INTO repository VALUES(?, ?, ?);",
                repo_record
            )
        self.db.executemany(
            "INSERT INTO repository_file VALUES(?, ?, ?);",
            [
                (2, "aabbccddeeff0000", "/tmp/file.txt"),
                (1, "12345678abcdabcd", "C:\\USER\\info.ini")
            ]
        )
        self.db.commit()
        
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
        
    def test_create_schema_ok(self):
        path = random_file_name()
        new_db = sqlite3.connect(path)
        db.create_schema(new_db)
        created = sqlite3.connect(path)
        for table in ALL_TABLES:
            self.assertTrue(
                db.has_table(created, table),
                msg=f"Table {table} not found after create schema."
            )
        created.close()
        os.remove(path)
        
    def test_insert_file_ok(self):
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
        
    def test_insert_file_with_repo_ok(self):
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
        result = self.db.execute(f"SELECT * FROM repository_file WHERE id_file='{md5}';")
        results = result.fetchall()
        self.assertIn(
            (1, md5, path),
            results,
            msg="Entry not found in 'repository_file' table."
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
        result = self.db.execute(f"SELECT * FROM repository WHERE id={id_repo};")
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
        expected = [record[0] for record in TEST_FILE_RECORDS]
        obtained = db.list_of_files(self.db)
        self.assertEqual(
            set(expected),
            set(obtained),
            msg="Set of obtained and returned md5's are different."
        )
        
    def test_list_of_repositories_ok(self):
        self.fillDb()
        expected = [(int(t[0]), t[1], t[2]) for t in TEST_REPO_RECORDS]
        obtained = db.list_of_repository(self.db)
        self.assertEqual(
            set(expected),
            set(obtained),
            msg="Set of obtained and returned repositories differ."
        )
        
    
        
        
