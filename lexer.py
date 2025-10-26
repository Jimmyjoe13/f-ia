# lexer.py
import re
from errors import LexerError

class Token:
    def __init__(self, type_token, valeur, ligne=0, colonne=0):
        self.type = type_token
        self.valeur = valeur
        self.ligne = ligne
        self.colonne = colonne

    def __repr__(self):
        return f"Token({self.type}, {self.valeur}, L{self.ligne}, C{self.colonne})"

class LexerFIA:
    def __init__(self, code_source):
        self.code = code_source
        self.position = 0
        self.ligne = 1
        self.colonne = 1
        self.tokens = []

        # Mots-clés (SUPPRIMÉ RACINE, PUISSANCE, etc. - ce sont des fonctions, pas des mots-clés)
        self.mots_cles = {
            'soit': 'SOIT',
            'si': 'SI',
            'sinon': 'SINON',
            'pour': 'POUR',
            'dans': 'DANS',
            'tant_que': 'TANT_QUE',
            'fonction': 'FONCTION',
            'retourner': 'RETOURNER',
            'vrai': 'VRAI',
            'faux': 'FAUX',
            'nul': 'NUL',
            'et': 'ET',
            'ou': 'OU',
            'non': 'NON',
            'essayer': 'ESSAYER',
            'attraper': 'ATTRAPER',
            # === MOTS-CLÉS MODULES ===
            'importer': 'IMPORTER',
            'depuis': 'DEPUIS',
            'comme': 'COMME',
            'de': 'DE',
            # SUPPRIMÉ : racine, puissance, arrondir, aleatoire, etc. 
            # Ce sont des fonctions intégrées, pas des mots-clés !
        }

        # Symboles et opérateurs
        self.symboles = {
            '=': 'ASSIGNATION',
            '==': 'EGAL',
            '!=': 'DIFF',
            '<': 'INF',
            '<=': 'INF_EGAL',
            '>': 'SUP',
            '>=': 'SUP_EGAL',
            '+': 'PLUS',
            '-': 'MOINS',
            '*': 'FOIS',
            '/': 'DIVISE',
            '%': 'MODULO',
            '(': 'PARENTHESE_OUVRANTE',
            ')': 'PARENTHESE_FERMANTE',
            '{': 'ACCOLADE_OUVRANTE',
            '}': 'ACCOLADE_FERMANTE',
            '[': 'CROCHET_OUVRANT',
            ']': 'CROCHET_FERMANT',
            '.': 'POINT',
            ',': 'VIRGULE',
            ':': 'DEUX_POINTS',
            ';': 'POINT_VIRGULE',
            # Opérateurs d'assignation composés
            '+=': 'PLUS_EGAL',
            '-=': 'MOINS_EGAL',
            '*=': 'FOIS_EGAL',
            '/=': 'DIVISE_EGAL',
            '%=': 'MODULO_EGAL',
        }

    def tokeniser(self):
        while self.position < len(self.code):
            char = self.code[self.position]

            # Espaces
            if char.isspace():
                if char == '\n':
                    self.ligne += 1
                    self.colonne = 1
                else:
                    self.colonne += 1
                self.avancer()
                continue

            # Commentaires: # ... fin de ligne
            if char == '#':
                self.ignorer_commentaire_ligne()
                continue

            # Commentaires: // ... fin de ligne (AVANT symboles!)
            if char == '/' and self.position + 1 < len(self.code) and self.code[self.position + 1] == '/':
                self.avancer()  # avance sur le premier '/'
                self.avancer()  # avance sur le deuxième '/'
                self.ignorer_commentaire_ligne()
                continue

            # Identifiants / Mots-clés
            if char.isalpha() or char == '_' or self.est_accentue(char):
                self.traiter_mot_cle_ou_identifiant()
                continue

            # Nombres
            if char.isdigit():
                self.traiter_nombre()
                continue

            # Chaînes
            if char in ['"', "'"]:
                self.traiter_chaine()
                continue

            # Symboles (APRÈS commentaires //)
            if self.traiter_symbole():
                continue

            # Caractère inconnu
            raise LexerError(f"Caractère inconnu '{char}' à la ligne {self.ligne}, colonne {self.colonne}")

        # Token de fin
        self.tokens.append(Token('EOF', '', self.ligne, self.colonne))
        return self.tokens

    def est_accentue(self, char):
        return '\u00C0' <= char <= '\u017F'

    def avancer(self):
        if self.position < len(self.code):
            if self.code[self.position] == '\n':
                self.ligne += 1
                self.colonne = 1
            else:
                self.colonne += 1
            self.position += 1

    def regarder(self, distance=1):
        """Regarde le caractère à une certaine distance sans avancer"""
        pos = self.position + distance - 1
        if pos < len(self.code):
            return self.code[pos]
        return ''

    def ignorer_commentaire_ligne(self):
        # Ignore jusqu'au prochain '\n' ou fin de fichier
        while self.position < len(self.code) and self.code[self.position] != '\n':
            self.avancer()

    def traiter_mot_cle_ou_identifiant(self):
        debut = self.position
        while self.position < len(self.code) and (
            self.code[self.position].isalnum() or
            self.code[self.position] == '_' or
            self.est_accentue(self.code[self.position])
        ):
            self.avancer()
        lexeme = self.code[debut:self.position]
        type_token = self.mots_cles.get(lexeme, 'IDENTIFIANT')
        self.tokens.append(Token(type_token, lexeme, self.ligne, self.colonne_calcul(debut, lexeme)))

    def traiter_nombre(self):
        debut = self.position
        point_rencontre = False
        while self.position < len(self.code):
            c = self.code[self.position]
            if c.isdigit():
                self.avancer()
            elif c == '.' and not point_rencontre:
                point_rencontre = True
                self.avancer()
            else:
                break
        lexeme = self.code[debut:self.position]
        valeur = float(lexeme) if '.' in lexeme else int(lexeme)
        self.tokens.append(Token('NOMBRE', valeur, self.ligne, self.colonne_calcul(debut, lexeme)))

    def traiter_chaine(self):
        quote_type = self.code[self.position]
        debut = self.position
        self.avancer()  # passer l'ouverture
        while self.position < len(self.code) and self.code[self.position] != quote_type:
            if self.code[self.position] == '\n':
                raise LexerError(f"Chaîne non terminée à la ligne {self.ligne}")
            self.avancer()
        if self.position >= len(self.code):
            raise LexerError("Chaîne non terminée à la fin du fichier")
        self.avancer()  # passer la fermeture
        lexeme = self.code[debut:self.position]
        valeur = lexeme[1:-1]
        self.tokens.append(Token('CHAINE', valeur, self.ligne, self.colonne_calcul(debut, lexeme)))

    def traiter_symbole(self):
        # Vérifier d'abord les symboles à 2 caractères (+=, -=, etc.)
        deux_car = self.code[self.position:self.position+2]
        if deux_car in self.symboles:
            self.tokens.append(Token(self.symboles[deux_car], deux_car, self.ligne, self.colonne))
            self.avancer()
            self.avancer()
            return True

        # Puis les symboles à 1 caractère
        un_car = self.code[self.position]
        if un_car in self.symboles:
            self.tokens.append(Token(self.symboles[un_car], un_car, self.ligne, self.colonne))
            self.avancer()
            return True
        return False

    def colonne_calcul(self, debut, lexeme):
        return self.colonne

# Exemple d'utilisation
if __name__ == "__main__":
    code = """
    # Test nouveau lexer avec imports
    importer "utils/math.fia" comme math
    depuis "collections.fia" importer liste_triee
    
    soit x = 10
    pour nom dans noms {
        imprimer(nom)
    }
    x += 5
    racine(x)  // Maintenant c'est un identifiant, pas un mot-clé
    """
    lexer = LexerFIA(code)
    tokens = lexer.tokeniser()
    for token in tokens:
        print(token)
