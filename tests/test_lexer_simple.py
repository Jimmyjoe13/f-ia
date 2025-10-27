# test_lexer_simple.py
from lexer import LexerFIA

code = '''importer "lib/math.fia" comme math
soit x = 5
imprimer(math.carre(x))'''

print("🧪 Test du lexer:")
print(f"Code à analyser:\n{code}\n")

lexer = LexerFIA(code)
tokens = lexer.tokeniser()

print("Tokens générés:")
for token in tokens:
    print(f"  {token}")
