from engine.database import Database
from engine.parser import Parser
from engine.executor import Executor

db = Database()
parser = Parser()
executor = Executor(db)

print("Mini RDBMS started. Type 'exit' to quit.")

while True:
    q = input("db> ")
    if q.lower() == "exit":
        break
    try:
        cmd = parser.parse(q)
        result = executor.execute(cmd)
        if isinstance(result, list):
            for r in result:
                print(r)
        else:
            print(result)
    except Exception as e:
        print("Error:", e)
