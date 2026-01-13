# where tables live

from engine.table import Table

class Database:
    def __init__(self):
        self.tables = {}

    def create_table(self, name, columns, primary_key=None, unique_cols=None):
        if name in self.tables:
            raise ValueError('Table already exists')

        self.tables[name] = Table(
            name, columns, primary_key, unique_cols
        )

    def get_table(self, name):
        if name not in self.tables:
            raise ValueError('Table not found')
        return self.tables[name]
