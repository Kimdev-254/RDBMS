from engine.tokenizer import tokenize
from engine.parser import parse
from engine.database import Database
from engine.executor import Executor

def main():
    db = Database()
    executor = Executor(db)

    print("Mini RDBMS started. Type 'exit' to quit.")

    while True:
        try:
            sql = input('db> ').strip()
            if sql.lower() in ('exit', 'quit'):
                break

            tokens = tokenize(sql)
            ast = parse(tokens)
            result = executor.execute(ast)
            print(result)

        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()
