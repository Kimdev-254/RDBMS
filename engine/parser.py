import re

class Parser:
    def parse(self, query):
        query = query.strip().rstrip(";")

        if query.upper().startswith("CREATE TABLE"):
            return self._parse_create(query)

        if query.upper().startswith("INSERT"):
            return self._parse_insert(query)

        if query.upper().startswith("SELECT"):
            return self._parse_select(query)

        raise ValueError("Unsupported query")

    def _parse_create(self, query):
        match = re.match(r"CREATE TABLE (\w+)\s*\((.+)\)", query, re.IGNORECASE)
        if not match:
            raise ValueError("Invalid CREATE TABLE syntax")

        table = match.group(1)
        cols_raw = match.group(2).split(",")

        columns = []
        primary_key = None
        unique_cols = []

        for col in cols_raw:
            parts = col.strip().split()
            name = parts[0]
            columns.append(name)

            if "PRIMARY" in parts:
                primary_key = name
            if "UNIQUE" in parts:
                unique_cols.append(name)

        return {
            "type": "CREATE",
            "table": table,
            "columns": columns,
            "primary_key": primary_key,
            "unique": unique_cols,
        }

    def _parse_insert(self, query):
        match = re.match(r"INSERT INTO (\w+) VALUES\s*\((.+)\)", query, re.IGNORECASE)
        if not match:
            raise ValueError("Invalid INSERT syntax")

        values = []
        for v in match.group(2).split(","):
            v = v.strip()
            if v.startswith("'") and v.endswith("'"):
                values.append(v[1:-1])
            else:
                values.append(int(v))

        return {
            "type": "INSERT",
            "table": match.group(1),
            "values": values,
        }

    def _parse_select(self, query):
        join = re.match(
            r"SELECT \* FROM (\w+) JOIN (\w+) ON (\w+)\.(\w+) = (\w+)\.(\w+)",
            query,
            re.IGNORECASE,
        )

        if join:
            return {
                "type": "JOIN",
                "left": join.group(1),
                "right": join.group(2),
                "left_col": join.group(4),
                "right_col": join.group(6),
            }

        simple = re.match(
            r"SELECT \* FROM (\w+)(?: WHERE (\w+) = '?(.*?)'?)?$",
            query,
            re.IGNORECASE,
        )

        if simple:
            where = None
            if simple.group(2):
                where = (simple.group(2), "=", simple.group(3))
            return {
                "type": "SELECT",
                "table": simple.group(1),
                "where": where,
            }

        raise ValueError("Invalid SELECT syntax")
