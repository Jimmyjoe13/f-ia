# fia_repl.py - Version avec listes, tableaux, fonctions, portée, et retourner
import re
import sys
import math
import random

print("🚀 Démarrage de F-IA REPL...")

# Exception spécifique pour gérer le 'retourner'
class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

# ==================== LEXER CORRIGÉ ====================
class LexerFIA:
    def __init__(self):
        self.tokens = []
        self.rules = [
            # Mots-clés français
            ('SOIT', r'\bsoit\b'),
            ('SI', r'\bsi\b'),
            ('SINON', r'\bsinon\b'),
            ('POUR', r'\bpour\b'),
            ('TANT_QUE', r'\btant_que\b'),
            ('FONCTION', r'\bfonction\b'),
            ('RETOURNER', r'\bretourner\b'),
            ('VRAI', r'\bvrai\b'),
            ('FAUX', r'\bfaux\b'),
            ('NUL', r'\bnul\b'),
            ('ESSAYER', r'\bessayer\b'),
            ('ATTRAPER', r'\battraper\b'),
            ('IMPORTER', r'\bimporter\b'),
            ('DE', r'\bde\b'),
            
            # Opérateurs et symboles
            ('EGAL', r'=='),
            ('DIFF', r'!='),
            ('INF_EGAL', r'<='),
            ('SUP_EGAL', r'>='),
            ('PLUS', r'\+'),
            ('MOINS', r'-'),
            ('FOIS', r'\*'),
            ('DIVISE', r'/'),
            ('MODULO', r'%'),
            ('ET', r'et\b'),
            ('OU', r'ou\b'),
            
            # Symboles simples
            ('ASSIGNATION', r'='),
            ('INF', r'<'),
            ('SUP', r'>'),
            ('PARENTHESE_OUVRANTE', r'\('),
            ('PARENTHESE_FERMANTE', r'\)'),
            ('ACCOLADE_OUVRANTE', r'\{'),
            ('ACCOLADE_FERMANTE', r'\}'),
            ('CROCHET_OUVRANT', r'\['),
            ('CROCHET_FERMANT', r'\]'),
            ('POINT', r'\.'),
            ('VIRGULE', r','),
            ('DEUX_POINTS', r':'),
            ('POINT_VIRGULE', r';'),
            
            # Littéraux
            ('IDENTIFIANT', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('ENTIER', r'\d+'),
            ('DECIMAL', r'\d+\.\d+'),
            ('CHAINE', r'"[^"]*"|\'[^\']*\''),
            
            # Ignorer les espaces et commentaires
            ('IGNORER', r'[ \t\n]+'),
            ('COMMENTAIRE', r'//[^\n]*|/\*.*?\*/'),
        ]

    def tokeniser(self, code_source):
        """Transforme le code source en liste de tokens"""
        self.tokens = []
        position = 0
        
        while position < len(code_source):
            match_trouve = False
            
            for nom_token, pattern in self.rules:
                regex = re.compile(pattern)
                match = regex.match(code_source, position)
                
                if match:
                    if nom_token not in ['IGNORER', 'COMMENTAIRE']:
                        valeur = match.group()
                        self.tokens.append((nom_token, valeur))
                    
                    position = match.end()
                    match_trouve = True
                    break
            
            if not match_trouve:
                # Afficher le contexte de l'erreur
                debut = max(0, position - 10)
                fin = min(len(code_source), position + 10)
                contexte = code_source[debut:fin]
                raise SyntaxError(f"Caractère inattendu: '{code_source[position]}' à la position {position}\nContexte: ...{contexte}...")
        
        return self.tokens

# ==================== PARSER AVEC LISTES - CORRIGÉ ====================
class ParserFIA:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.current_token = tokens[0] if tokens else None
        self._erreur_log = []  # Pour stocker les erreurs rencontrées pendant le parsing

    def _ajouter_erreur(self, message):
        """Enregistre une erreur de parsing sans lancer d'exception."""
        if self.current_token:
            pos = self.position
            token_valeur = self.current_token[1] if self.current_token else "EOF"
            self._erreur_log.append(f"Erreur à la position {pos} (token: '{token_valeur}'): {message}")
        else:
            self._erreur_log.append(f"Erreur: {message}")

    def advance(self):
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = None

    def peek(self):
        """Regarde le token suivant"""
        if self.position + 1 < len(self.tokens):
            return self.tokens[self.position + 1]
        return None

    def parse(self):
        """Parse les tokens"""
        statements = []
        while self.current_token:
            try:
                stmt = self._parse_single_statement()
                if stmt:
                    statements.append(stmt)
            except Exception as e:
                # Même si une exception est levée, on tente d'avancer pour éviter la boucle infinie
                self._ajouter_erreur(f"Exception lors du parsing d'une instruction: {e}")
                self.advance() # Avancer pour ne pas rester bloqué
        # Afficher les erreurs en fin de parsing
        if self._erreur_log:
            for erreur in self._erreur_log:
                print(f"⚠️  {erreur}")
        return statements

    def _parse_single_statement(self):
        """Parse une seule instruction. Cette fonction est enveloppée dans parse() pour gérer les erreurs."""
        if self.current_token[0] == 'SOIT':
            return self.parse_declaration()
        elif self.current_token[0] == 'SI':
            return self.parse_if_statement()
        elif self.current_token[0] == 'TANT_QUE':
            return self.parse_while_statement()
        elif self.current_token[0] == 'POUR':
            return self.parse_for_statement()
        elif self.current_token[0] == 'FONCTION': # Ajout pour la future implémentation
            return self.parse_function_definition()
        elif self.current_token[0] == 'RETOURNER':
            return self.parse_return_statement() # Ajout pour la nouvelle fonctionnalité
        elif self.current_token[0] == 'IDENTIFIANT' and self.peek() and self.peek()[0] == 'PARENTHESE_OUVRANTE':
            return self.parse_function_call()
        else:
            # Essayer de parser une expression (y compris les assignations)
            # Si elle commence par un identifiant, ce pourrait être une réassignation (x = 5)
            if self.current_token[0] == 'IDENTIFIANT':
                # Vérifier si le suivant est une ASSIGNATION
                if self.peek() and self.peek()[0] == 'ASSIGNATION':
                    return self.parse_assignment()
                else:
                    # Sinon, c'est peut-être une expression de fonction ou une variable seule
                    expr = self.parse_expression()
                    if expr:
                        # Consommer un point-virgule s'il est présent
                        if self.current_token and self.current_token[0] == 'POINT_VIRGULE':
                            self.advance()
                        return ('EXPRESSION', expr)
            else:
                # Pour les autres types de tokens au début d'une instruction
                expr = self.parse_expression()
                if expr:
                    # Consommer un point-virgule s'il est présent
                    if self.current_token and self.current_token[0] == 'POINT_VIRGULE':
                        self.advance()
                    return ('EXPRESSION', expr)
            # Si aucune instruction claire n'est trouvée, on avance pour ne pas bloquer
            self._ajouter_erreur(f"Instruction inconnue ou inattendue: '{self.current_token[1] if self.current_token else 'EOF'}'")
            self.advance()
            return None # Retourne None pour indiquer qu'aucune instruction valide n'a été trouvée ici


    def parse_assignment(self):
        """Parse une assignation comme x = 5 ou x = y + 1"""
        # On suppose que le token courant est un IDENTIFIANT
        if not self.current_token or self.current_token[0] != 'IDENTIFIANT':
            raise SyntaxError("Assignation attendue avec un identifiant")
        nom_variable = self.current_token[1]
        self.advance() # Consommer le nom de la variable

        if not self.current_token or self.current_token[0] != 'ASSIGNATION':
            raise SyntaxError("Signe '=' attendu dans l'assignation")
        self.advance() # Consommer le '='

        valeur = self.parse_expression()
        return ('ASSIGNMENT', ('VARIABLE', nom_variable), valeur)

    # --- Nouvelle fonction pour le mot-clé 'retourner' ---
    def parse_return_statement(self):
        """Parse: retourner expression"""
        self.advance() # Consommer 'retourner'
        valeur = self.parse_expression() # L'expression est optionnelle, mais on la parse si présente
        return ('RETURN', valeur)


    def parse_declaration(self):
        """Parse: soit x = 10"""
        self.advance()  # 'soit'
        if not self.current_token or self.current_token[0] != 'IDENTIFIANT':
            raise SyntaxError("Identifiant attendu après 'soit'")
        
        nom = self.current_token[1]
        self.advance()
        
        valeur = None
        if self.current_token and self.current_token[0] == 'ASSIGNATION':
            self.advance()  # '='
            valeur = self.parse_expression()
            
        return ('DECLARATION', nom, valeur)

    def parse_if_statement(self):
        """Parse condition SI"""
        self.advance()  # 'si'
        if not self.current_token or self.current_token[0] != 'PARENTHESE_OUVRANTE':
            raise SyntaxError("'( attendu après 'si'")
        self.advance()
        
        condition = self.parse_expression()
        
        if not self.current_token or self.current_token[0] != 'PARENTHESE_FERMANTE':
            raise SyntaxError("')' attendu après condition")
        self.advance()
        
        if not self.current_token or self.current_token[0] != 'ACCOLADE_OUVRANTE':
            raise SyntaxError("'{' attendu après condition")
        self.advance()
        
        # Parse bloc
        bloc = self.parse_block()
        
        if not self.current_token or self.current_token[0] != 'ACCOLADE_FERMANTE':
            raise SyntaxError("'}' attendu pour fermer le bloc")
        self.advance()
        
        # Gestion de 'sinon' optionnel
        else_bloc = None
        if self.current_token and self.current_token[0] == 'SINON':
            self.advance() # Consommer 'sinon'
            if not self.current_token or self.current_token[0] != 'ACCOLADE_OUVRANTE':
                raise SyntaxError("'{' attendu après 'sinon'")
            self.advance()
            else_bloc = self.parse_block()
            if not self.current_token or self.current_token[0] != 'ACCOLADE_FERMANTE':
                raise SyntaxError("'}' attendu pour fermer le bloc 'sinon'")
            self.advance()

        return ('IF', condition, bloc, else_bloc)

    def parse_while_statement(self):
        """Parse boucle TANT_QUE"""
        self.advance()  # 'tant_que'
        if not self.current_token or self.current_token[0] != 'PARENTHESE_OUVRANTE':
            raise SyntaxError("'( attendu après 'tant_que'")
        self.advance()
        
        condition = self.parse_expression()
        
        if not self.current_token or self.current_token[0] != 'PARENTHESE_FERMANTE':
            raise SyntaxError("')' attendu après condition")
        self.advance()
        
        if not self.current_token or self.current_token[0] != 'ACCOLADE_OUVRANTE':
            raise SyntaxError("'{' attendu après condition")
        self.advance()
        
        # Parse bloc
        bloc = self.parse_block()
        
        if not self.current_token or self.current_token[0] != 'ACCOLADE_FERMANTE':
            raise SyntaxError("'}' attendu pour fermer le bloc")
        self.advance()
        
        return ('WHILE', condition, bloc)

    def parse_for_statement(self):
        """Parse boucle POUR"""
        self.advance()  # 'pour'
        if not self.current_token or self.current_token[0] != 'PARENTHESE_OUVRANTE':
            raise SyntaxError("'( attendu après 'pour'")
        self.advance()
        
        # Initialisation
        init = None
        if self.current_token and self.current_token[0] == 'SOIT':
            init = self.parse_declaration()
        elif self.current_token and self.current_token[0] == 'IDENTIFIANT' and self.peek() and self.peek()[0] == 'ASSIGNATION':
             init = self.parse_assignment()
        else:
            # Si aucune initialisation standard, on la considère comme vide ou on la parse comme une expression
            init = self.parse_expression() # ou on la passe
            if not self.current_token or self.current_token[0] != 'POINT_VIRGULE':
                 raise SyntaxError("';' attendu après initialisation")
        
        if not self.current_token or self.current_token[0] != 'POINT_VIRGULE':
            raise SyntaxError("';' attendu après initialisation")
        self.advance()
        
        # Condition
        condition = self.parse_expression()
        
        if not self.current_token or self.current_token[0] != 'POINT_VIRGULE':
            raise SyntaxError("';' attendu après condition")
        self.advance()
        
        # Incrément
        increment = self.parse_expression()
        
        if not self.current_token or self.current_token[0] != 'PARENTHESE_FERMANTE':
            raise SyntaxError("')' attendu après incrément")
        self.advance()
        
        if not self.current_token or self.current_token[0] != 'ACCOLADE_OUVRANTE':
            raise SyntaxError("'{' attendu après boucle")
        self.advance()
        
        # Parse bloc
        corps = self.parse_block()
        
        if not self.current_token or self.current_token[0] != 'ACCOLADE_FERMANTE':
            raise SyntaxError("'}' attendu pour fermer le bloc")
        self.advance()
        
        return ('FOR', init, condition, increment, corps)

    def parse_block(self):
        """Parse un bloc d'instructions"""
        statements = []
        while self.current_token and self.current_token[0] != 'ACCOLADE_FERMANTE':
            # Ignorer les point-virgules seuls
            if self.current_token[0] == 'POINT_VIRGULE':
                self.advance()
                continue
                
            # Appeler la même logique que pour une instruction unique
            try:
                stmt = self._parse_single_statement()
                if stmt:
                    statements.append(stmt)
            except Exception as e:
                # Si une erreur survient dans une instruction du bloc, on la log et on continue
                self._ajouter_erreur(f"Erreur dans le bloc: {e}")
                self.advance() # Avancer pour ne pas bloquer
                # Optionnel: Ajouter une instruction vide ou une instruction d'erreur au bloc
                # statements.append(('ERROR_STATEMENT', str(e)))
                
        return statements

    def parse_function_call(self):
        """Parse appel de fonction"""
        nom = self.current_token[1]
        self.advance()  # nom de fonction
        
        if not self.current_token or self.current_token[0] != 'PARENTHESE_OUVRANTE':
            raise SyntaxError("'( attendu après nom de fonction")
        self.advance()
        
        arguments = []
        while self.current_token and self.current_token[0] != 'PARENTHESE_FERMANTE':
            if self.current_token[0] == 'VIRGULE':
                self.advance()
                if self.current_token and self.current_token[0] not in ['PARENTHESE_FERMANTE']: # Eviter [func(,)]
                    arg = self.parse_expression()
                    if arg:
                        arguments.append(arg)
            else:
                arg = self.parse_expression()
                if arg:
                    arguments.append(arg)
        
        if not self.current_token or self.current_token[0] != 'PARENTHESE_FERMANTE':
            raise SyntaxError("')' attendu après arguments")
        self.advance()
        
        return ('FUNCTION_CALL', nom, arguments)

    # Ajout de la fonction pour les définitions de fonctions (préparation future)
    def parse_function_definition(self):
        """Parse: fonction nom(...) { ... }"""
        self.advance() # Consommer 'fonction'
        if not self.current_token or self.current_token[0] != 'IDENTIFIANT':
            raise SyntaxError("Nom de fonction attendu")
        nom_fonction = self.current_token[1]
        self.advance() # Consommer le nom

        if not self.current_token or self.current_token[0] != 'PARENTHESE_OUVRANTE':
            raise SyntaxError("'(' attendu après le nom de la fonction")
        self.advance() # Consommer '('

        # Parser les paramètres
        params = []
        if self.current_token and self.current_token[0] != 'PARENTHESE_FERMANTE':
            if self.current_token[0] == 'IDENTIFIANT':
                params.append(self.current_token[1])
                self.advance()
                while self.current_token and self.current_token[0] == 'VIRGULE':
                    self.advance() # Consommer ','
                    if self.current_token and self.current_token[0] == 'IDENTIFIANT':
                        params.append(self.current_token[1])
                        self.advance()
                    else:
                        raise SyntaxError("Nom de paramètre attendu après ','")
            elif self.current_token[0] != 'PARENTHESE_FERMANTE':
                 raise SyntaxError("Nom de paramètre ou ')' attendu")

        if not self.current_token or self.current_token[0] != 'PARENTHESE_FERMANTE':
            raise SyntaxError("')' attendu après les paramètres")
        self.advance() # Consommer ')'

        if not self.current_token or self.current_token[0] != 'ACCOLADE_OUVRANTE':
            raise SyntaxError("'{' attendu après la signature de la fonction")
        self.advance() # Consommer '{'

        # Parser le corps de la fonction
        corps = self.parse_block()

        if not self.current_token or self.current_token[0] != 'ACCOLADE_FERMANTE':
            raise SyntaxError("'}' attendu pour fermer le corps de la fonction")
        self.advance() # Consommer '}'

        # Retourne un nœud spécial pour la définition de fonction
        return ('FUNCTION_DEFINITION', nom_fonction, params, corps)


    def parse_expression(self):
        """Parse une expression complète"""
        return self.parse_assignment_expression() # Appel de la nouvelle fonction

    # Renommage de l'ancienne parse_assignment pour éviter les confusions
    def parse_assignment_expression(self):
        """Parse les assignations et les expressions de base"""
        left = self.parse_logical_or()
        
        # Vérifier si c'est une assignation
        if self.current_token and self.current_token[0] == 'ASSIGNATION':
            self.advance()  # consommer '='
            right = self.parse_assignment_expression() # Récursion pour gérer a = b = c
            return ('ASSIGNMENT', left, right)
        
        return left

    # Nouvelle hiérarchie d'opérateurs pour une meilleure gestion
    def parse_logical_or(self):
        left = self.parse_logical_and()
        while self.current_token and self.current_token[0] == 'OU':
            op = self.current_token[1]
            self.advance()
            right = self.parse_logical_and()
            left = ('BINARY_OP', op, left, right)
        return left

    def parse_logical_and(self):
        left = self.parse_equality()
        while self.current_token and self.current_token[0] == 'ET':
            op = self.current_token[1]
            self.advance()
            right = self.parse_equality()
            left = ('BINARY_OP', op, left, right)
        return left

    def parse_equality(self):
        left = self.parse_relational()
        while self.current_token and self.current_token[0] in ['EGAL', 'DIFF']:
            op = self.current_token[1]
            self.advance()
            right = self.parse_relational()
            left = ('BINARY_OP', op, left, right)
        return left

    def parse_relational(self):
        left = self.parse_addition()
        while self.current_token and self.current_token[0] in ['INF', 'SUP', 'INF_EGAL', 'SUP_EGAL']:
            op = self.current_token[1]
            self.advance()
            right = self.parse_addition()
            left = ('BINARY_OP', op, left, right)
        return left

    def parse_addition(self):
        left = self.parse_multiplication()
        
        while self.current_token and self.current_token[0] in ['PLUS', 'MOINS']:
            op = self.current_token[1]
            self.advance()
            right = self.parse_multiplication()
            left = ('BINARY_OP', op, left, right)
        
        return left

    def parse_multiplication(self):
        left = self.parse_unary()
        
        while self.current_token and self.current_token[0] in ['FOIS', 'DIVISE', 'MODULO']:
            op = self.current_token[1]
            self.advance()
            right = self.parse_unary()
            left = ('BINARY_OP', op, left, right)
        
        return left

    def parse_unary(self):
        # Gestion des opérateurs unaires (ex: -5, !vrai) si implémentés
        # Pour l'instant, on passe directement à la primaire
        return self.parse_primary()

    def parse_primary(self):
        """Parse éléments primaires"""
        if not self.current_token:
            return None
            
        token = self.current_token
        
        if token[0] in ['ENTIER', 'DECIMAL']:
            self.advance()
            return ('NUMBER', token[1])
        elif token[0] == 'IDENTIFIANT':
            ident = token[1]
            self.advance()
            
            # Vérifier si c'est un appel de fonction
            if self.current_token and self.current_token[0] == 'PARENTHESE_OUVRANTE':
                self.advance()
                arguments = []
                
                # Parser les arguments
                if self.current_token and self.current_token[0] != 'PARENTHESE_FERMANTE':
                    arguments.append(self.parse_expression())
                    while self.current_token and self.current_token[0] == 'VIRGULE':
                        self.advance()
                        arguments.append(self.parse_expression())
                
                if not self.current_token or self.current_token[0] != 'PARENTHESE_FERMANTE':
                    raise SyntaxError("Parenthèse fermante attendue après arguments")
                self.advance()
                
                return ('FUNCTION_CALL', ident, arguments)
            else:
                return ('VARIABLE', ident)
                
        elif token[0] == 'CHAINE':
            self.advance()
            return ('STRING', token[1])
        elif token[0] == 'VRAI':
            self.advance()
            return ('BOOLEAN', True)
        elif token[0] == 'FAUX':
            self.advance()
            return ('BOOLEAN', False)
        elif token[0] == 'CROCHET_OUVRANT':
            return self.parse_list()
        elif token[0] == 'PARENTHESE_OUVRANTE':
            self.advance()
            expr = self.parse_expression()
            if not self.current_token or self.current_token[0] != 'PARENTHESE_FERMANTE':
                raise SyntaxError("Parentèse fermante manquante")
            self.advance()
            return expr
        else:
            raise SyntaxError(f"Expression inattendue: {token}")

    def parse_list(self):
        """Parse une liste [element1, element2, ...]"""
        self.advance()  # consommer '['
        elements = []
        
        # Si la liste n'est pas vide
        if self.current_token and self.current_token[0] != 'CROCHET_FERMANT':
            elements.append(self.parse_expression())
            while self.current_token and self.current_token[0] == 'VIRGULE':
                self.advance()
                elements.append(self.parse_expression())
        
        if not self.current_token or self.current_token[0] != 'CROCHET_FERMANT':
            raise SyntaxError("']' attendu pour fermer la liste")
        self.advance()
        
        return ('LIST', elements)

# ==================== ÉVALUATEUR AVEC LISTES ET RETOURNER ====================
class EvaluateurFIA:
    def __init__(self):
        # Utilisation d'une pile de contextes pour la portée des variables
        self.contextes = [{}]  # Pile de dictionnaires. Le premier est le contexte global.
        self.fonctions_integrees = self.initialiser_fonctions_integrees()
        # Pour stocker les fonctions définies par l'utilisateur
        self.fonctions_definies = {}

    def initialiser_fonctions_integrees(self):
        """Initialise les fonctions intégrées"""
        return {
            'imprimer': self.fonction_imprimer,
            'longueur': self.fonction_longueur,
            'arrondir': self.fonction_arrondir,
            'aleatoire': self.fonction_aleatoire,
            'racine': self.fonction_racine,
            'puissance': self.fonction_puissance,
            'entier': self.fonction_entier,
            'chaine': self.fonction_chaine,
        }

    def fonction_imprimer(self, *args):
        """Affiche les arguments"""
        resultat = " ".join(str(arg) for arg in args)
        print(f"📢 {resultat}")
        return resultat

    def fonction_longueur(self, obj):
        """Retourne la longueur d'un objet"""
        if isinstance(obj, list):
            return len(obj)
        else:
            return len(str(obj))

    def fonction_arrondir(self, nombre, decimales=0):
        """Arrondit un nombre"""
        return round(nombre, decimales)

    def fonction_aleatoire(self):
        """Génère un nombre aléatoire entre 0 et 1"""
        return random.random()

    def fonction_racine(self, nombre):
        """Calcule la racine carrée"""
        return math.sqrt(nombre)

    def fonction_puissance(self, base, exposant):
        """Calcule la puissance"""
        return math.pow(base, exposant)

    def fonction_entier(self, valeur):
        """Convertit en entier"""
        return int(valeur)

    def fonction_chaine(self, valeur):
        """Convertit en chaîne"""
        return str(valeur)

    def evaluer(self, ast):
        """Évalue l'AST"""
        resultat = None
        for node in ast:
            resultat = self.eval_node(node)
        return resultat

    def _get_variable(self, nom):
        """Recherche une variable dans la pile des contextes."""
        for contexte in reversed(self.contextes): # Recherche du plus local au plus global
            if nom in contexte:
                return contexte[nom]
        raise NameError(f"Variable '{nom}' non définie")

    def _set_variable(self, nom, valeur):
        """Définit une variable dans le contexte local actuel."""
        if self.contextes: # S'assure qu'il y a au moins un contexte
            self.contextes[-1][nom] = valeur # Affecte dans le contexte du haut de la pile
        else:
            # Cas improbable si la pile est toujours initialisée
            self.contextes[0][nom] = valeur


    def eval_node(self, node):
        """Évalue un nœud individuel de l'AST"""
        if not node:
            return None
            
        node_type = node[0]
        
        if node_type == 'DECLARATION':
            nom = node[1]
            valeur = self.eval_node(node[2]) if node[2] is not None else None
            self._set_variable(nom, valeur)
            print(f"✅ Variable '{nom}' = {valeur}")
            return valeur
            
        elif node_type == 'IF':
            condition = self.eval_node(node[1])
            if condition:
                print("🔨 Exécution du bloc SI")
                for stmt in node[2]:
                    self.eval_node(stmt)
            elif node[3]: # else_bloc
                print("🔨 Exécution du bloc SINON")
                for stmt in node[3]:
                    self.eval_node(stmt)
            return None
            
        elif node_type == 'WHILE':
            condition = self.eval_node(node[1])
            compteur = 0
            while condition and compteur < 50:
                print(f"🔁 Itération {compteur + 1}")
                for stmt in node[2]:
                    self.eval_node(stmt)
                
                condition = self.eval_node(node[1])
                compteur += 1
                
            if compteur >= 50:
                print("🛑 Sécurité: boucle arrêtée après 50 itérations")
            else:
                print("✅ Boucle TANT_QUE terminée")
            return None
            
        elif node_type == 'FOR':
            if node[1]:
                self.eval_node(node[1])
            
            condition = self.eval_node(node[2])
            compteur = 0
            while condition and compteur < 50:
                print(f"🔁 Itération {compteur + 1}")
                
                for stmt in node[4]:
                    self.eval_node(stmt)
                
                self.eval_node(node[3])
                condition = self.eval_node(node[2])
                compteur += 1
                
            if compteur >= 50:
                print("🛑 Sécurité: boucle arrêtée après 50 itérations")
            else:
                print("✅ Boucle POUR terminée")
            return None

        elif node_type == 'FUNCTION_DEFINITION':
            nom = node[1]
            params = node[2]
            corps = node[3]
            # Stocker la définition de la fonction
            self.fonctions_definies[nom] = {'params': params, 'corps': corps}
            print(f"✅ Fonction '{nom}' définie avec {len(params)} paramètre(s)")
            return None # Une définition ne retourne pas de valeur

        # --- Gestion du mot-clé 'retourner' ---
        elif node_type == 'RETURN':
            valeur = self.eval_node(node[1]) if node[1] is not None else None
            # Lever une exception pour sortir de la fonction
            raise ReturnException(valeur)
            
        elif node_type == 'ASSIGNMENT':
            # Gestion des assignations: variable = valeur
            target = node[1]
            value = self.eval_node(node[2])
            
            if target[0] == 'VARIABLE':
                nom_variable = target[1]
                self._set_variable(nom_variable, value)
                print(f"✅ Assignation: {nom_variable} = {value}")
                return value
            else:
                raise SyntaxError("La cible d'assignation doit être une variable")
            
        elif node_type == 'EXPRESSION':
            return self.eval_node(node[1])
            
        elif node_type == 'FUNCTION_CALL':
            nom_fonction = node[1]
            arguments = [self.eval_node(arg) for arg in node[2]]
            
            if nom_fonction in self.fonctions_integrees:
                return self.fonctions_integrees[nom_fonction](*arguments)
            elif nom_fonction in self.fonctions_definies:
                 # Appel d'une fonction définie par l'utilisateur
                 func_def = self.fonctions_definies[nom_fonction]
                 params = func_def['params']
                 corps = func_def['corps']

                 if len(arguments) != len(params):
                     raise TypeError(f"Erreur: la fonction '{nom_fonction}' attend {len(params)} arguments, {len(arguments)} fournis.")
                 
                 # Créer un contexte local pour les paramètres
                 contexte_local = {}
                 for param, arg in zip(params, arguments):
                     contexte_local[param] = arg

                 # Sauvegarder le contexte global
                 ancien_contexte = self.contextes
                 # Remplacer la pile par un nouveau contexte local
                 self.contextes = [contexte_local]

                 resultat_fonction = None
                 try:
                     for stmt in corps:
                         self.eval_node(stmt)
                 except ReturnException as e:
                     # Récupérer la valeur de retour si 'retourner' est exécuté
                     resultat_fonction = e.value
                 # Si la boucle se termine sans 'retourner', la fonction retourne None
                 # Restaurer le contexte global
                 self.contextes = ancien_contexte
                 return resultat_fonction
            else:
                raise NameError(f"Fonction '{nom_fonction}' non définie")
            
        elif node_type == 'LIST':
            # Évalue chaque élément de la liste
            elements = [self.eval_node(element) for element in node[1]]
            print(f"✅ Liste créée: {elements}")
            return elements
            
        elif node_type == 'BINARY_OP':
            operateur = node[1]
            gauche = self.eval_node(node[2])
            droite = self.eval_node(node[3])
            
            # Conversion des types
            gauche = self.convertir_si_nombre(gauche)
            droite = self.convertir_si_nombre(droite)
                
            if operateur == '+':
                resultat = gauche + droite
            elif operateur == '-':
                resultat = gauche - droite
            elif operateur == '*':
                resultat = gauche * droite
            elif operateur == '/':
                if droite == 0:
                    raise ZeroDivisionError("Division par zéro")
                resultat = gauche / droite
            elif operateur == '%':
                resultat = gauche % droite
            elif operateur == '==':
                resultat = gauche == droite
            elif operateur == '!=':
                resultat = gauche != droite
            elif operateur == '<':
                resultat = gauche < droite
            elif operateur == '>':
                resultat = gauche > droite
            elif operateur == '<=':
                resultat = gauche <= droite
            elif operateur == '>=':
                resultat = gauche >= droite
            elif operateur == 'et': # Logique
                resultat = gauche and droite
            elif operateur == 'ou': # Logique
                resultat = gauche or droite
            else:
                raise ValueError(f"Opérateur non supporté: {operateur}")
            
            print(f"✅ {gauche} {operateur} {droite} = {resultat}")
            return resultat
            
        elif node_type == 'NUMBER':
            if '.' in node[1]:
                return float(node[1])
            else:
                return int(node[1])
                
        elif node_type == 'STRING':
            return node[1][1:-1] # Enlève les guillemets
            
        elif node_type == 'BOOLEAN':
            return node[1]
            
        elif node_type == 'VARIABLE':
            return self._get_variable(node[1]) # Utilisation de la nouvelle méthode
        
        return None

    def convertir_si_nombre(self, valeur):
        """Convertit une valeur en nombre si possible"""
        if isinstance(valeur, str):
            if valeur.replace('.', '').replace('-', '').isdigit():
                return float(valeur) if '.' in valeur else int(valeur)
        return valeur

# ==================== REPL COMPLET ====================
class REPLFIA:
    def __init__(self):
        self.lexer = LexerFIA()
        self.evaluateur = EvaluateurFIA()
        
    def demarrer(self):
        self.afficher_bienvenue()
        
        while True:
            try:
                ligne = input("f-ia> ").strip()
                
                if self.gerer_commandes_speciales(ligne):
                    continue
                    
                if ligne:
                    self.traiter_ligne(ligne)
                    
            except KeyboardInterrupt:
                print("\n🛑 Utilisez 'quitter' pour sortir")
            except EOFError:
                print("\n👋 Au revoir !")
                break
            except Exception as e:
                print(f"❌ Erreur: {e}")

    def afficher_bienvenue(self):
        print("🌟" * 50)
        print("🤖 F-IA v0.1 - REPL Interactif")
        print("💻 Langage de programmation français pour l'IA")
        print("🎯 Maintenant avec LISTES et TABLEAUX!")
        print("🌟" * 50)
        print("Commandes: .aide, .variables, .reset, .quitter")
        print("🌟" * 50)

    def gerer_commandes_speciales(self, ligne):
        ligne = ligne.strip()
        
        if ligne == ".aide":
            self.afficher_aide()
            return True
        elif ligne == ".variables":
            self.lister_variables()
            return True
        elif ligne == ".reset":
            # Réinitialiser les contextes : un contexte global vide
            self.evaluateur.contextes = [{}]
            # Réinitialiser les fonctions définies par l'utilisateur
            self.evaluateur.fonctions_definies = {}
            print("🔄 Variables et fonctions réinitialisées")
            return True
        elif ligne in [".quitter", "quitter"]:
            print("👋 Au revoir !")
            sys.exit(0)
        return False

    def traiter_ligne(self, ligne):
        try:
            tokens = self.lexer.tokeniser(ligne)
            print(f"🔤 Tokens: {tokens}")
            
            parser = ParserFIA(tokens)
            ast = parser.parse()
            print(f"🌳 AST: {ast}")
            
            resultat = self.evaluateur.evaluer(ast)
            if resultat is not None:
                print(f"🎯 Résultat: {resultat}")
                
        except Exception as e:
            print(f"❌ {e}")

    def afficher_aide(self):
        print("\n📚 AIDE F-IA:")
        print("  soit liste = [1, 2, 3]")
        print("  longueur(liste)")
        print("  soit x = 10")
        print("  x = x + 1")
        print("  si (x > 5) { imprimer(\"Grand\") }")
        print("  tant_que (i < 3) { imprimer(i); i = i + 1 }")
        print("  fonction doubler(n) { retourner n * 2; }") # Exemple avec 'retourner'

    def lister_variables(self):
        if not self.evaluateur.contextes[0]: # Vérifie le contexte global
            print("📝 Aucune variable globale")
        else:
            print("\n📝 Variables globales:")
            for nom, valeur in self.evaluateur.contextes[0].items(): # Accès au contexte global
                print(f"  {nom} = {valeur}")
        if not self.evaluateur.fonctions_definies:
            print("📝 Aucune fonction définie")
        else:
            print("\n📝 Fonctions définies:")
            for nom, _ in self.evaluateur.fonctions_definies.items():
                print(f"  {nom}")


if __name__ == "__main__":
    try:
        repl = REPLFIA()
        repl.demarrer()
    except Exception as e:
        print(f"💥 Erreur: {e}")
