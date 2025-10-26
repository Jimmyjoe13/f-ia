# test_racine_simple.py
from lexer import LexerFIA

# Test simple avec racine
code = '''soit x = 9
soit resultat = racine(x)
imprimer(resultat)'''

print("🧪 Test lexer avec racine:")
print(f"Code:\n{code}\n")

lexer = LexerFIA(code)
tokens = lexer.tokeniser()

print("Tokens:")
for token in tokens:
    print(f"  {token}")
