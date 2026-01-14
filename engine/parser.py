def parse(tokens):
    if not tokens:
        raise SyntaxError("Empty input")

    first = tokens[0][1]

    if first == 'SELECT':
        return parse_select(tokens)
    if first == 'CREATE':
        return parse_create(tokens)

    raise SyntaxError(f"Unsupported statement: {first}")


# =========================
# SELECT
# =========================
def parse_select(tokens):
    i = 0

    # SELECT
    i += 1

    # COLUMNS
    columns = []
    if tokens[i][1] == '*':
        columns.append('*')
        i += 1
    else:
        while True:
            if tokens[i][0] != 'IDENT':
                raise SyntaxError("Expected column name")
            columns.append(tokens[i][1])
            i += 1
            if i < len(tokens) and tokens[i][1] == ',':
                i += 1
                continue
            break

    # FROM
    if tokens[i][1] != 'FROM':
        raise SyntaxError("Expected FROM")
    i += 1

    # TABLE
    table = tokens[i][1]
    i += 1

    # OPTIONAL WHERE
    where = None
    if i < len(tokens) and tokens[i][1] == 'WHERE':
        i += 1
        col = tokens[i][1]; i += 1
        op = tokens[i][1]; i += 1
        val_type, val = tokens[i]
        if val_type == 'NUMBER':
            val = int(val)
        i += 1
        where = (col, op, val)

    return {
        'type': 'SELECT',
        'columns': columns,
        'table': table,
        'where': where
    }


# =========================
# CREATE TABLE
# =========================
def parse_create(tokens):
    i = 0

    # CREATE
    i += 1

    if tokens[i][1] != 'TABLE':
        raise SyntaxError("Expected TABLE")
    i += 1

    # table name
    table_name = tokens[i][1]
    i += 1

    if tokens[i][1] != '(':
        raise SyntaxError("Expected (")
    i += 1

    columns = []
    primary_key = None
    unique_cols = []

    while True:
        col_name = tokens[i][1]
        i += 1

        col_type = tokens[i][1]
        i += 1

        # constraints
        if i < len(tokens) and tokens[i][1] == 'PRIMARY':
            i += 1
            if tokens[i][1] != 'KEY':
                raise SyntaxError("Expected KEY")
            i += 1
            primary_key = col_name

        elif i < len(tokens) and tokens[i][1] == 'UNIQUE':
            unique_cols.append(col_name)
            i += 1

        columns.append(col_name)

        if tokens[i][1] == ',':
            i += 1
            continue

        if tokens[i][1] == ')':
            i += 1
            break

        raise SyntaxError("Invalid CREATE TABLE syntax")

    return {
        'type': 'CREATE_TABLE',
        'table': table_name,
        'columns': columns,
        'primary_key': primary_key,
        'unique_cols': unique_cols
    }
