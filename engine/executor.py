# Executor - taes the AST (dictionary creayed by the parser)

class Executor:
    def __init__(self, db):
        self.db = db

    def execute(self, ast):
        if ast['type'] == 'SELECT':
            return self._select(ast)

        if ast['type'] == 'CREATE_TABLE':
            return self._create_table(ast)

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
