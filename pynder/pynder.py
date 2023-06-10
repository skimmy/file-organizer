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

import hashlib
import os
import sys
import sqlite3

from db import list_of_files, list_of_repository, has_schema, create_schema


# def list_to_db(files, db_name):
#     con = sqlite3.connect(db_name)
#     cur = con.cursor()
#     cur.execute(
#         "SELECT name FROM sqlite_master WHERE type='table' AND name='file';")
#     table_exists = cur.fetchone() is not None
#     if not table_exists:
#         cur.execute("CREATE TABLE file (md5, path);")
#     cur.executemany("INSERT INTO file VALUES(?, ?)", files)
#     con.commit()
#     con.close()


# def md5_for_file(path):
#     if not os.path.isfile(path):
#         raise IOError(f'File not found: ${path}')
#     content = None
#     with open(path, 'rb') as f:
#         content = f.read()
#     if not content:
#         raise Exception('Unable to read file content')
#     h = hashlib.new('md5')
#     h.update(content)
#     return h.hexdigest()


def for_each_file(path, operation, recursive=True):
    dirs = []
    for item in os.scandir(path):
        if item.is_dir():
            dirs.append(item.path)
        if item.is_file(follow_symlinks=False):
            operation(item.path)
    if recursive:
        for d in dirs:
            for_each_file(d, operation, recursive)


def db_for_dir(dir_path, db_path):
    files = []
    for_each_file(dir_path, lambda x: files.append(
        (md5_for_file(x), x)), recursive=True)
    list_to_db(files, db_path)


def open_or_create_db(path: str, overwrite: bool = True) -> sqlite3.Connection:
    connection = sqlite3.connect(path)
    if (not has_schema(connection.cursor())) and overwrite:
        create_schema(connection)
    return connection

def add_repo(path: str, desc: str):
    # Add repo first
    pass

    # Scan and add each file

def main():
    file = os.path.expanduser("~/.pynder.sqlite")
    if (len(sys.argv) > 1):
        file = sys.argv[1]
    print(f"Using file {file}")
    print()
    con = open_or_create_db(file)
    running = True
    while running:
        command = input(f"{os.path.basename(file)}> ")
        if command.lower() == 'help' or command.lower() == 'h':
            print()
            print("  Available commands")
            print("  ------------------")
            print("     q | quit  --> Exit the program")
            print("     h | help  --> Show this message")
            print("     f | file  --> Show file table")
            print("     r | repo  --> Show repository table")
            print("     addrepo   --> Scan directory 'd' and adds to repo")
            print()
        elif command.lower() == 'quit' or command.lower() == 'q':
            print("     Bye Bye...\n")
            running = False
        elif command.lower() == 'file' or command.lower() == 'f':
            records = list_of_files(con)
            for record in records:
                print("      ", record)
            print(f"      {len(records)} Total record(s)")
        elif command.lower() == 'repo' or command.lower() == 'r':
            records = list_of_repository(con)
            print(f"      {len(records)} Total repositories")
        elif command.lower() == 'addrepo':
            path = input(f"      Directory")
            desc = input(f"      Description")
            add_repo(con, path, desc)
        else:
            print(f"      Command '{command}' not recognized, type 'h' for help.")
    con.close()

if __name__ == '__main__':
    main()
