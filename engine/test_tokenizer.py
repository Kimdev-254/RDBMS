from engine.tokenizer import tokenize

sql = "SELECT name FROM users WHERE id = 1;"
tokens = tokenize(sql)

for t in tokens:
    print(t)
