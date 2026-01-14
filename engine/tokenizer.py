# tokenizer(sql -> tokens)

import re

TOKEN_SPEC = [
    ('NUMBER',  r'\d+'),
    ('STRING',  r"'[^']*'"),
    ('IDENT',   r'[A-Za-z_][A-Za-z0-9_]*'),
    ('OP',      r'=|<|>'),
    ('SKIP',    r'[ \t\n]+'),
    ('SYMBOL',  r'[(),;*]'),
]

KEYWORDS = {
    'SELECT', 'FROM', 'WHERE', 'INSERT', 'INTO',
    'VALUES', 'CREATE', 'TABLE', 'PRIMARY',
    'KEY', 'UNIQUE', 'UPDATE', 'SET', 'DELETE',
    'JOIN', 'ON'
}

def tokenize(sql):
    tokens = []
    pos = 0

    while pos < len(sql):
        match = None
        for name, regex in TOKEN_SPEC:
            pattern = re.compile(regex)
            match = pattern.match(sql, pos)
            if match:
                text = match.group(0)
                if name == 'IDENT' and text.upper() in KEYWORDS:
                    tokens.append(('KEYWORD', text.upper()))
                elif name != 'SKIP':
                    tokens.append((name, text.strip("'")))
                pos = match.end()
                break
        if not match:
            raise SyntaxError(f'Unexpected character: {sql[pos]}')

    return tokens
