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

"""Some utility functions used by the testing modules."""
import os
import random
import shutil
import sqlite3

import pynder.db as dbu

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


def random_file_name(prefix: str = ".test", ext: str = None, separator: str = "_") -> str:
    """Creates string that can be used as a random name.

    The name is obtained concatenating `prefix`, `separator` a 9-digits random number and
    `extension` (if indicated).

    Args:
        prefix (str, optional): The prefix of the nme. Defaults to ".test".
        ext (str, optional): The extension to be used. Defaults to None.
        separator (str, optional): String separator to be used. Defaults to "_".

    Returns:
        str: The string with the random generated number.
    """
    rand = random.randint(100000000, 999999999)
    extension = ""
    if ext:
        extension = f".{ext}"
    return f"{prefix}{separator}{rand}{extension}"


def create_testing_dir(root_dir="./dist", sub_dir="subdir"):
    """Creates and populates a directory for testing purposes.

    The function fills the directory with at least three files (two with
    same content but different name) and one non-empty subdirectory.

    Args:
        root_dir (str, optional): The path of the directory to create. Defaults to "./dist".
        sub_dir (str, optional): The name of a subdirectory to create. Defaults to "subdir".
    """
    os.mkdir(root_dir)

    file1_path = os.path.join(root_dir, "file1.txt")
    file2_path = os.path.join(root_dir, "file2.jpg")
    file3_path = os.path.join(root_dir, "file3.txt")

    # Write some content to the files
    with open(file1_path, "w") as file1:
        file1.write("Hello World!")
    with open(file2_path, "wb") as file2:
        file2.write("File 2 content".encode())
    with open(file3_path, "w") as file3:
        file3.write("File 3 content")

    # Create another file with the same content as file1 but with a different name
    file4_path = os.path.join(root_dir, "file4.txt")
    shutil.copyfile(file1_path, file4_path)

    # Create a subdirectory
    sub_dir = os.path.join(root_dir, sub_dir)
    os.mkdir(sub_dir)

    # Create a file inside the subdirectory
    sub_file_path = os.path.join(sub_dir, "subfile.txt")
    with open(sub_file_path, "w") as sub_file:
        sub_file.write("Subfile content")

    # Print the directory structure
    for root, dirs, files in os.walk(root_dir):
        level = root.replace(root_dir, "").count(os.sep)
        indent = " " * 4 * (level)
        print("{}{}/".format(indent, os.path.basename(root)))
        subindent = " " * 4 * (level + 1)
        for f in files:
            print("{}{}".format(subindent, f))


def fill_testing_db(db: sqlite3.Connection) -> None:
    """Fills the passed DB with testing data.
    
    This function should be called with an empty DB as it will attempt
    to create a schema and fill some values on the tables. It may fail
    if some of the operations during creation or filling fail.

    Args:
        db (sqlite3.Connection): The DB to be filled
    """
    dbu.create_schema(db)
    for file_record in TEST_FILE_RECORDS:
        db.execute(
            "INSERT INTO file VALUES(?, ?);",
            file_record
        )
    for repo_record in TEST_REPO_RECORDS:
        db.execute(
            "INSERT INTO repository VALUES(?, ?, ?);",
            repo_record
        )
    db.executemany(
        "INSERT INTO repository_file VALUES(?, ?, ?);",
        [
            (2, "aabbccddeeff0000", "/tmp/file.txt"),
            (1, "12345678abcdabcd", "C:\\USER\\info.ini")
        ]
    )
    db.commit()
