class Executor:
    def __init__(self, db):
        self.db = db

    def execute(self, ast):
        if ast['type'] == 'SELECT':
            return self._select(ast)

        if ast['type'] == 'CREATE_TABLE':
            return self._create_table(ast)

        if ast['type'] == 'INSERT':
            return self._insert(ast)

        if ast['type'] == 'UPDATE':
            return self._update(ast)

        if ast['type'] == 'DELETE':
            return self._delete(ast)

        raise ValueError("Unknown AST type")

    def _select(self, ast):
        table = self.db.get_table(ast['table'])
        rows = table.select(ast['where'])

        if ast['columns'] != ['*']:
            rows = [
                {c: r[c] for c in ast['columns']}
                for r in rows
            ]
        return rows

    def _create_table(self, ast):
        self.db.create_table(
            ast['table'],
            ast['columns'],
            ast['primary_key'],
            ast['unique_cols']
        )
        return f"Table '{ast['table']}' created"

    def _insert(self, ast):
        table = self.db.get_table(ast['table'])

        if len(ast['values']) != len(table.columns):
            raise ValueError("Column count does not match values")

        row = dict(zip(table.columns, ast['values']))
        table.insert(row)

        return "1 row inserted"

    def _update(self, ast):
        table = self.db.get_table(ast['table'])
        col, new_val = ast['set']
        where = ast['where']

        count = 0
        for row in table.rows:
            if where[1] == '=' and row[where[0]] == where[2]:
                row[col] = new_val
            count += 1

        return f"{count} row(s) updated"

    def _delete(self, ast):
        table = self.db.get_table(ast['table'])
        col, op, val = ast['where']

        before = len(table.rows)
        table.rows = [
            r for r in table.rows
            if not (op == '=' and r[col] == val)
        ]
        deleted = before - len(table.rows)

        return f"{deleted} row(s) deleted"

