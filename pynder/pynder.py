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
import sys

from db import list_of_files, list_of_repository, has_schema, create_schema
from task import add_repo

def open_or_create_db(path: str, overwrite: bool = True) -> sqlite3.Connection:
    connection = sqlite3.connect(path)
    if (not has_schema(connection.cursor())) and overwrite:
        create_schema(connection)
    return connection

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
            path = input(f"      Directory: ")
            desc = input(f"      Description: ")
            add_repo(con, os.path.abspath(path), desc)
        else:
            print(f"      Command '{command}' not recognized, type 'h' for help.")
    con.close()

if __name__ == '__main__':
    main()
