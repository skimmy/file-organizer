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
    ("12345678abcdabcd", "/tmp", None),
    ("9876543210112233", "C:\\example.pdf", 1),
    ("aabbccddeeff0000", "/home/users/", 2)
]

class DbTest(unittest.TestCase):
    
    def setUp(self):
        self.db_name = random_file_name(ext="sqlite")
        self.db = sqlite3.connect(self.db_name)
    
    def fillDb(self):
        db.create_schema(self.db)
        for file_record in TEST_FILE_RECORDS:
            self.db.execute(
                "INSERT INTO file VALUES(?, ?, ?);",
                file_record
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
    
    def test_list_of_files_ok(self):
        self.fillDb()
        expected = [record[0] for record in TEST_FILE_RECORDS]
        obtained = db.list_of_files(self.db)
        self.assertEqual(
            set(expected),
            set(obtained),
            msg="Set of obtained and returned md5's are different."
        )
        
    
        
        
