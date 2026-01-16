class Table:
    def __init__(self, name, columns, primary_key=None, unique_cols=None):
        self.name = name
        self.columns = columns
        self.primary_key = primary_key
        self.unique_cols = unique_cols or []
        self.rows = []
        self.indexes = {}

        if primary_key:
            self.create_index(primary_key)
        for col in self.unique_cols:
            self.create_index(col)

    def create_index(self, column):
        self.indexes[column] = {}
        for row in self.rows:
            self.indexes[column][row[column]] = row

    def insert(self, values):
        row = dict(zip(self.columns, values))

        if self.primary_key:
            pk = row[self.primary_key]
            if pk in self.indexes[self.primary_key]:
                raise ValueError("Primary key violation")

        for col in self.unique_cols:
            if row[col] in self.indexes[col]:
                raise ValueError(f"Unique constraint violation on {col}")

        self.rows.append(row)

        for col, idx in self.indexes.items():
            idx[row[col]] = row

    def select(self, where=None):
        if not where:
            return self.rows

        col, op, val = where

        if col in self.indexes and op == "=":
            row = self.indexes[col].get(val)
            return [row] if row else []

        return [r for r in self.rows if r[col] == val]
