import sqlite3
import os
import sys
import datetime


class Database:
    """ class to manage I/O with database """

    _UTC_OFFSET_TIMEDELTA = (datetime.datetime.utcnow() - datetime.datetime.now()).total_seconds()

    class _Decorator(object):
        """ private decorator methods"""

        @classmethod
        def transaction(cls, func):
            def wrapper(*args):
                db = args[0]
                with sqlite3.connect(db._path) as conn:
                    db._cursor = conn.cursor()
                    func(*args)
                db._cursor = None
                conn.commit()

            return wrapper

    def __init__(self, path):
        sys.stderr.write("initializing database wth path %s\n" % (path,))
        self._path = path
        self._cursor = None
        self.results = None

    @_Decorator.transaction
    def _create_table(self, schema):
        sys.stderr.write(schema.name)
        query = """CREATE TABLE %s %s""" % (schema.name, str(schema))
        sys.stderr.write("%s\n" % (query,))
        self._cursor.execute(query)
        sys.stderr.write("%s table created\n" % (schema.name,))

    @_Decorator.transaction
    def _make_query(self, query):
        sys.stderr.write(query + '\n')
        self._cursor.execute(query)
        self.results = []
        for i in self._cursor:
            self.results.append(i)

    @_Decorator.transaction
    def _insert_query(self, query):
        sys.stderr.write(query + '\n')
        self._cursor.execute(query)
        sys.stderr.write("Last row id {}\n".format(self._cursor.lastrowid))
        self.results = []
        self.results.append((self._cursor.lastrowid,))

    def _read_data_into_table(self, file_path, columns, table_name):
        path = os.path.join(os.path.dirname(__file__), file_path)
        with open(path, "r") as read:
            rows = read.readlines()[1:]
            for line in rows:
                line = line.strip()
                data = line.split(',')
                query = "INSERT OR IGNORE INTO %s %s VALUES %s" % (
                    table_name,
                    columns,
                    str(tuple(data)) if len(data) > 1 else "('{}')".format(data[0])
                )
                self._insert_query(query)












