class Executor:
    def __init__(self, db):
        self.db = db

    def execute(self, cmd):
        t = cmd["type"]

        if t == "CREATE":
            self.db.create_table(
                cmd["table"],
                cmd["columns"],
                cmd["primary_key"],
                cmd["unique"],
            )
            return "Table created"

        if t == "INSERT":
            table = self.db.get_table(cmd["table"])
            table.insert(cmd["values"])
            return "Row inserted"

        if t == "SELECT":
            table = self.db.get_table(cmd["table"])
            return table.select(cmd["where"])

        if t == "JOIN":
            return self._join(cmd)

        raise ValueError("Unknown command")

    def _join(self, cmd):
        left = self.db.get_table(cmd["left"])
        right = self.db.get_table(cmd["right"])

        results = []

        if cmd["right_col"] in right.indexes:
            idx = right.indexes[cmd["right_col"]]
            for l in left.rows:
                r = idx.get(l[cmd["left_col"]])
                if r:
                    results.append({**l, **r})
            return results

        for l in left.rows:
            for r in right.rows:
                if l[cmd["left_col"]] == r[cmd["right_col"]]:
                    results.append({**l, **r})

        return results
