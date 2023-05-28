# Pynder file organizer

A file organizer written in Python

## Using the tool (Under development)
Currently, `pynder` offers a REPL only interface, run the following command to fire the interactive console.

```console
python pynder.py [db.sqlite]
```

The file `db.sqlite` is opened and all operations are then performed on such a database. If the indicated file doesn't exist it is created with a new schema. If the file exists, but the database is in the wrong format, the program terminates with an error. The indication of the database file can be omitted, in which case a *user global* database is opened (or created if non-exiting).

## Run all tests

To run, in *verbose* mode, all the tests available in the `test` folder
run the following command from the root project directory

```console
python -m unittest discover test -v
```