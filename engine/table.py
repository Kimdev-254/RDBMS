class Table:
    def __init__(self, name, columns, primary_key=None, unique_cols=None):
        self.name = name
        self.columns = columns
        self.primary_key = primary_key
        self.unique_cols = unique_cols or []
        self.rows = []

        # indexes: column_name -> { value -> list of rows }
        self.indexes = {}
        if primary_key:
            self.create_index(primary_key)
        for col in self.unique_cols:
            self.create_index(col)

    def create_index(self, column):
        self.indexes[column] = {}
        for row in self.rows:
            val = row[column]
            self.indexes[column][val] = row

    def insert(self, row):
        # enforce primary key
        if self.primary_key:
            pk_val = row[self.primary_key]
            if pk_val in self.indexes[self.primary_key]:
                raise ValueError("Primary key violation")

        # enforce unique constraints
        for col in self.unique_cols:
            val = row[col]
            if val in self.indexes[col]:
                raise ValueError(f"Unique constraint failed on {col}")

        self.rows.append(row)

        # update indexes
        for col, idx in self.indexes.items():
            idx[row[col]] = row

    def select(self, where=None):
        if where:
            col, op, val = where
            if col in self.indexes and op == '=':
                row = self.indexes[col].get(val)
                return [row] if row else []
            # fallback to full scan
            return [
                r for r in self.rows
                if op == '=' and r[col] == val
            ]
        return self.rows
