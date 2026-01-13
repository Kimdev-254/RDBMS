# REPL - It cooordinates the three main phases of query processing: Tokenizing, Parsing, and Executing

from engine.tokenizer import tokenize
from engine.parser import parse_select
from engine.database import Database
from engine.executor import Executor

db = Database()
executor = Executor(db)

while True:
    try:
        sql = input('db> ')
        if sql.lower() in ('exit', 'quit'):
            break

        tokens = tokenize(sql)
        ast = parse_select(tokens)
        result = executor.execute(ast)
        print(result)

    except Exception as e:
        print('Error:', e)
