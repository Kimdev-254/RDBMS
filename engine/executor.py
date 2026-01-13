# Executor - taes the AST (dictionary creayed by the parser)

class Executor:
    def __init__(self, db):
        self.db = db

    def execute(self, ast):
        if ast['type'] == 'SELECT':
            table = self.db.get_table(ast['table'])
            rows = table.select(ast['where'])

            if ast['columns'] != ['*']:
                rows = [
                    {c: r[c] for c in ast['columns']}
                    for r in rows
                ]
            return rows
