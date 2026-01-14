from engine.table import Table

users = Table(
    name='users',
    columns=['id', 'email', 'name'],
    primary_key='id',
    unique_cols=['email']
)

users.insert({'id': 1, 'email': 'a@b.com', 'name': 'Alice'})
users.insert({'id': 2, 'email': 'b@b.com', 'name': 'Bob'})
users.insert({'id': 1, 'email': 'x@y.com', 'name': 'X'})

print(users.select())
print(users.select(('id', '=', 1)))
