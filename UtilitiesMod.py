import sqlite3
from os import getcwd, listdir,chdir
from os.path import isfile
from os import system
from sys import stderr


class DatabaseManager:
    """Context manager class that handles the database connections."""
    def __init__(self, database: str = 'ExpenseTrackerDatabase.db'):
        self.database = database

    def __enter__(self):
        self.con = sqlite3.connect(self.database)
        self.cur = self.con.cursor()
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cur.close()
        self.con.close()


def directory_files():
    """return a list of the files in the current working directory"""
    return [file for file in listdir(getcwd()) if isfile(file)]


def database_exists():
    return 'ExpenseTrackerDatabase.db' in directory_files()


def create_database():
    if not database_exists():
        create_table = ("CREATE TABLE IF NOT EXISTS 'Transactions' ("
                        "'category'   TEXT,\n"
                        "'amount'   REAL,\n"
                        "'date'   TEXT,\n"
                        "'note'   TEXT,\n"
                        "'type'   TEXT)"
                        )
        with DatabaseManager() as db:
            db.execute(create_table)
            db.connection.commit()
    else:
        print('database already exists')


def convert_ui(*args):
    uifiles = [file for file in directory_files() if file[-3:] == '.ui']
    if len(args) == 0:
        for file in uifiles:
            system(f'pyuic5 {file} -o {file[:-3] +  ".py"}')
    else:
        for file in args:
            if file in uifiles:
                system(f'pyuic5 {file} -o {file[:-3] + ".py"}')
            else:
                print(f"Can't fine {file} in the current working directory.", file=stderr)


if __name__ == '__main__':
    convert_ui('categories.ui')
