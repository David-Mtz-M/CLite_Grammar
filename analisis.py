# %%
import ply.lex as lex
import ply.yacc as yacc
from arbol import Literal

reserved = {
    'while': 'WHILE'
}

literals = ['+','-','*','/', '%', '(', ')', '<', '>', '=', '!', ';', '{', '}']
tokens = ['ID', 'INTLIT', 'FLOATLIT', 'EQ', 'NEQ', 'AND', 'OR', 'LE', 'GE'] + list(reserved.values())

t_ignore  = ' \t'



def t_FLOATLIT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INTLIT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reserved.get(t.value, 'ID')
     return t

def t_EQ(t):
    r'=='
    return t

def t_NEQ(t):
    r'!='
    return t

def t_LE(t):
    r'<='
    return t

def t_GE(t):
    r'>='
    return t

def t_AND(t):
    r'&&'
    return t

def t_OR(t):
    r'\|\|'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

start = 'WhileStatement'

def p_WhileStatement(p):
    '''
    WhileStatement : WHILE '(' Expression ')' Statement
    '''
    p[0] = ('while', p[3], p[5])

def p_Statement(p):
    '''
    Statement : '{' StatementList '}'
              | Expression ';'
    '''
    p[0] = ('block', p[2]) if len(p) == 4 else ('expr', p[1])

def p_StatementList(p):
    '''
    StatementList : StatementList Statement
                  | Statement
    '''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_Expression(p):
    '''
    Expression : Expression OR Conjunction
               | Conjunction
    '''
    p[0] = ('or', p[1], p[3]) if len(p) == 4 else p[1]

def p_Conjunction(p):
    '''
    Conjunction : Conjunction AND Equality
                | Equality
    '''
    p[0] = ('and', p[1], p[3]) if len(p) == 4 else p[1]

def p_Equality(p):
    '''
    Equality : Relation EQ Relation
             | Relation NEQ Relation
             | Relation
    '''
    p[0] = (p[2], p[1], p[3]) if len(p) == 4 else p[1]

def p_Relation(p):
    '''
    Relation : Addition '<' Addition
             | Addition '>' Addition
             | Addition LE Addition
             | Addition GE Addition
             | Addition
    '''
    p[0] = (p[2], p[1], p[3]) if len(p) == 4 else p[1]

def p_Addition(p):
    '''
    Addition : Addition '+' Term
             | Addition '-' Term
             | Term
    '''
    p[0] = (p[2], p[1], p[3]) if len(p) == 4 else p[1]

def p_Term(p):
    '''
    Term : Term '*' Factor
         | Term '/' Factor
         | Term '%' Factor
         | Factor
    '''
    p[0] = (p[2], p[1], p[3]) if len(p) == 4 else p[1]

def p_Factor(p):
    '''
    Factor : '-' Primary
           | '!' Primary
           | Primary
    '''
    p[0] = (p[1], p[2]) if len(p) == 3 else p[1]

def p_Primary(p):
    '''
    Primary : ID
            | INTLIT
            | FLOATLIT 
            | '(' Expression ')'
    '''
    if len(p) == 2:
        token_type = 'ID' if isinstance(p[1], str) and not str(p[1]).isdigit() else 'NUM'
        p[0] = Literal(p[1], token_type)
    else:
        p[0] = p[2]

        
def p_error(p):
    print("Syntax error in input!", p)


# %%
data = "while (x < 5) { (x + 1); (y * 2); }"
lexer = lex.lex()
parser = yacc.yacc()
parser.parse(data)

# %%
