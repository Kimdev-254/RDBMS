# Parser

def parse_select(tokens):
    i = 0
    assert tokens[i][1] == 'SELECT'
    i += 1

    columns = []
    while tokens[i][0] == 'IDENT':
        columns.append(tokens[i][1])
        i += 1
        if tokens[i][0] == 'SYMBOL' and tokens[i][1] == ',':
            i += 1

    assert tokens[i][1] == 'FROM'
    i += 1

    table = tokens[i][1]
    i += 1

    where = None
    if i < len(tokens) and tokens[i][1] == 'WHERE':
        i += 1
        col = tokens[i][1]; i += 1
        op = tokens[i][1]; i += 1
        val = int(tokens[i][1]); i += 1
        where = (col, op, val)

    return {
        'type': 'SELECT',
        'columns': columns,
        'table': table,
        'where': where
    }
