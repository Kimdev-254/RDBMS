# table representation

class Table:
    def __init__(self, name, columns, primary_key=None, unique_cols=None):
        self.name = name
        self.columns = columns            # ['id', 'email', 'name']
        self.rows = []                    # list of dicts
        self.primary_key = primary_key
        self.unique_cols = unique_cols or []
        self.indexes = {}                 # col -> dict(value -> row)

    def insert(self, row):
        # Constraint checks
        for col in self.unique_cols:
            for r in self.rows:
                if r[col] == row[col]:
                    raise ValueError(f'Unique constraint failed on {col}')

        if self.primary_key:
            for r in self.rows:
                if r[self.primary_key] == row[self.primary_key]:
                    raise ValueError('Primary key violation')

        self.rows.append(row)

    def select(self, where=None):
        if not where:
            return self.rows

        col, op, value = where
        result = []

        for r in self.rows:
            if op == '=' and r[col] == value:
                result.append(r)
        return result
