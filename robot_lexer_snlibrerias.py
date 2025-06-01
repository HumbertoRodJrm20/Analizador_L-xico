import re
from tabulate import tabulate

RESET = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'


TOKEN_PATTERNS = [
    # (Token, Tipo, Valor, Parametro)
    ('\n', 'Salto de linea'), # Salto de linea
    ('Robot', 'Palabra_r'), # inicializar un robot
    ('(b|r)[0-9]', 'Identificador'),
    ('\.', 'Punto'),
    ('base|cuerpo|garra|velocidad', 'Método'),
    ('iniciar|cerrarGarra|abrirGarra', 'Acción'),
    ('=', 'Operador'),
    ('(360|3[0-5][0-9]|[12]\d\d|\d\d|\d)', 'Valor'),
    (' ', 'Espacio'),
    ('\(|\)', 'Parentesis'),
    ('repetir|finRepetir', 'Bucle'),
    ('.', 'Desconocido')
]

class Lexer:
    def __init__(self, rules):
        self.rules = [(re.compile(pattern), name) for pattern, name in rules]

    def tokenize(self, text):
        pos = 0
        tokens = []
        while pos < len(text):
            match_found = False
            for pattern, token_name in self.rules:
                match = pattern.match(text, pos)
                if match:
                    tokens.append((token_name, match.group()))
                    pos = match.end()
                    match_found = True
                    break
            if not match_found:
                raise SyntaxError(f"Token inesperado en '{text[pos]}', {pos=}")
        return tokens
    
lexer = Lexer(TOKEN_PATTERNS)

# Codigo accediendo a funciones
code1 = """
+++
Robot b1
b1.iniciar()
b1.repetir(3)
b1.velocidad(50)
b1.base(180)
b1.cuerpo(45)
b1.garra(0)
b1.cuerpo(90)
b1.garra(90)
b1.cerrarGarra()
b1.abrirGarra()
b1.finRepetir()
"""
# Codigo accediendo a propiedades
code2 = """
Robot r1
r1.iniciar
r1.velocidad=50
r1.base=180
r1.cuerpo=45
r1.garra=0
r1.cuerpo=90
r1.garra=90
"""

def tabulate_tokens(code:str, colors:bool) -> dict:
    tokens = lexer.tokenize(code)

    if colors:
        headers = [f'{BLUE}Token{RESET}', f'{CYAN}Tipo{RESET}', f'{MAGENTA}Valor{RESET}', f'{RED}Parametro{RESET}']
    else:
        headers = ['Token', 'Tipo', 'Valor', 'Parametro']
    rows    = []

    for i, token in enumerate(tokens):
        type, token_name = token
        value = '-'
        parameter = '-'

        if type == 'Método':
            value = tokens[i+2][1]
            parameter = 'Si'

        if type not in ('Espacio', 'Salto de linea'):
            if colors:
                rows.append([f'{BLUE}{token_name}{RESET}', f'{CYAN}{type}{RESET}', f'{MAGENTA}{value}{RESET}', f'{RED}{parameter}{RESET}'])
            else:
                rows.append([token_name, type, value, parameter])
    return {
        'headers': headers,
        'rows': rows
    }

if __name__ == '__main__':
    table = tabulate_tokens(code1, True)
    print(tabulate(table['rows'], headers=table['headers']))