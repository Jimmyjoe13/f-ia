# parser.py
from lexer import Token
from fia_ast import *
from errors import ParseError

class ParserFIA:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.ligne_courante = 0

    def analyser(self):
        instructions = []
        while not self.est_a_la_fin() and not self.regarder_token().type == 'EOF':
            instruction = self.analyser_instruction()
            if instruction:
                instructions.append(instruction)
        return Programme(instructions)

    def est_a_la_fin(self):
        return self.position >= len(self.tokens)

    def regarder_token(self):
        if self.est_a_la_fin():
            return Token('EOF', '', 0, 0)
        return self.tokens[self.position]

    def consommer_token(self, type_attendu=None):
        token = self.regarder_token()
        if type_attendu and token.type != type_attendu:
            raise ParseError(
                f"Attendu '{type_attendu}', trouvé '{token.type}' ('{token.valeur}')",
                ligne=token.ligne,
                colonne=token.colonne
            )
        self.position += 1
        return token

    def analyser_instruction(self):
        token = self.regarder_token()
        
        # === NOUVELLES INSTRUCTIONS D'IMPORT ===
        if token.type == 'IMPORTER':
            return self.analyser_import_module()
        elif token.type == 'DEPUIS':
            return self.analyser_import_depuis()
        
        # === INSTRUCTIONS EXISTANTES ===
        elif token.type == 'SOIT':
            return self.analyser_declaration_variable()
        elif token.type == 'FONCTION':
            return self.analyser_fonction()
        elif token.type == 'RETOURNER':
            return self.analyser_retour()
        elif token.type == 'SI':
            return self.analyser_condition()
        elif token.type == 'TANT_QUE':
            return self.analyser_boucle_tant_que()
        elif token.type == 'POUR':
            return self.analyser_boucle_pour_ou_pour_dans()
        elif token.type == 'IDENTIFIANT':
            return self.analyser_instruction_identifiant()
        else:
            # Pour les expressions qui ne commencent pas par un identifiant
            expr = self.analyser_expression()
            if self.regarder_token().type == 'POINT_VIRGULE':
                self.consommer_token('POINT_VIRGULE')
            return ExpressionStatement(expr)

    # === NOUVELLES MÉTHODES POUR LES IMPORTS ===

    def analyser_import_module(self):
        """
        Analyse : importer "chemin/module.fia" [comme alias]
        """
        self.consommer_token('IMPORTER')
        
        # Récupérer le chemin du module (chaîne)
        token_chemin = self.consommer_token('CHAINE')
        chemin_module = token_chemin.valeur
        
        # Vérifier s'il y a un alias
        alias = None
        if self.regarder_token().type == 'COMME':
            self.consommer_token('COMME')
            token_alias = self.consommer_token('IDENTIFIANT')
            alias = token_alias.valeur
        
        # Point-virgule optionnel
        if self.regarder_token().type == 'POINT_VIRGULE':
            self.consommer_token('POINT_VIRGULE')
        
        return ImportModule(chemin_module, alias)

    def analyser_import_depuis(self):
        """
        Analyse : depuis "module.fia" importer element1 [comme alias1], element2 [comme alias2]
        """
        self.consommer_token('DEPUIS')
        
        # Récupérer le chemin du module
        token_chemin = self.consommer_token('CHAINE')
        chemin_module = token_chemin.valeur
        
        self.consommer_token('IMPORTER')
        
        # Liste des éléments à importer
        elements_importes = []
        
        # Premier élément
        nom_element = self.consommer_token('IDENTIFIANT').valeur
        alias_element = nom_element  # Par défaut, alias = nom
        
        if self.regarder_token().type == 'COMME':
            self.consommer_token('COMME')
            alias_element = self.consommer_token('IDENTIFIANT').valeur
        
        elements_importes.append((nom_element, alias_element))
        
        # Éléments supplémentaires
        while self.regarder_token().type == 'VIRGULE':
            self.consommer_token('VIRGULE')
            
            nom_element = self.consommer_token('IDENTIFIANT').valeur
            alias_element = nom_element
            
            if self.regarder_token().type == 'COMME':
                self.consommer_token('COMME')
                alias_element = self.consommer_token('IDENTIFIANT').valeur
            
            elements_importes.append((nom_element, alias_element))
        
        # Point-virgule optionnel
        if self.regarder_token().type == 'POINT_VIRGULE':
            self.consommer_token('POINT_VIRGULE')
        
        return ImportDepuis(chemin_module, elements_importes)

    # === MÉTHODES EXISTANTES (INCHANGÉES OU LÉGÈREMENT MODIFIÉES) ===

    def analyser_instruction_identifiant(self):
        # Analyser l'expression complète (identifiant + accès éventuels)
        expr = self.analyser_expression()
        
        # Vérifier le type d'assignation
        token_courant = self.regarder_token()
        
        if token_courant.type == 'ASSIGNATION':
            # Assignation normale
            self.consommer_token('ASSIGNATION')
            valeur = self.analyser_expression()
            if self.regarder_token().type == 'POINT_VIRGULE':
                self.consommer_token('POINT_VIRGULE')
            return Assignation(expr, valeur)
        elif token_courant.type in ['PLUS_EGAL', 'MOINS_EGAL', 'FOIS_EGAL', 'DIVISE_EGAL', 'MODULO_EGAL']:
            # Assignation composée
            operateur = self.consommer_token().valeur
            valeur = self.analyser_expression()
            if self.regarder_token().type == 'POINT_VIRGULE':
                self.consommer_token('POINT_VIRGULE')
            return AssignationComposee(expr, operateur, valeur)
        else:
            # Expression simple
            if self.regarder_token().type == 'POINT_VIRGULE':
                self.consommer_token('POINT_VIRGULE')
            return ExpressionStatement(expr)

    def analyser_boucle_pour_ou_pour_dans(self):
        self.consommer_token('POUR')
        
        if self.regarder_token().type == 'PARENTHESE_OUVRANTE':
            return self.analyser_boucle_pour_classique()
        elif self.regarder_token().type == 'IDENTIFIANT':
            return self.analyser_boucle_pour_dans()
        else:
            raise ParseError(f"Syntaxe de boucle 'pour' invalide", 
                           ligne=self.regarder_token().ligne,
                           colonne=self.regarder_token().colonne)

    def analyser_boucle_pour_classique(self):
        self.consommer_token('PARENTHESE_OUVRANTE')
        init = self.analyser_instruction()
        self.consommer_token('POINT_VIRGULE')
        condition = self.analyser_expression()
        self.consommer_token('POINT_VIRGULE')
        increment = self.analyser_instruction()
        self.consommer_token('PARENTHESE_FERMANTE')
        corps = self.analyser_bloc()
        return BouclePour(init, condition, increment, corps)

    def analyser_boucle_pour_dans(self):
        variable = self.consommer_token('IDENTIFIANT').valeur
        self.consommer_token('DANS')
        iterable = self.analyser_expression()
        corps = self.analyser_bloc()
        return BouclePourDans(variable, iterable, corps)

    def analyser_declaration_variable(self):
        self.consommer_token('SOIT')
        nom = self.consommer_token('IDENTIFIANT').valeur
        valeur = None
        if self.regarder_token().type == 'ASSIGNATION':
            self.consommer_token('ASSIGNATION')
            valeur = self.analyser_expression()
        if self.regarder_token().type == 'POINT_VIRGULE':
            self.consommer_token('POINT_VIRGULE')
        return DeclarationVariable(nom, valeur)

    def analyser_fonction(self):
        self.consommer_token('FONCTION')
        nom = self.consommer_token('IDENTIFIANT').valeur
        self.consommer_token('PARENTHESE_OUVRANTE')
        params = []
        if self.regarder_token().type != 'PARENTHESE_FERMANTE':
            params.append(self.consommer_token('IDENTIFIANT').valeur)
            while self.regarder_token().type == 'VIRGULE':
                self.consommer_token('VIRGULE')
                params.append(self.consommer_token('IDENTIFIANT').valeur)
        self.consommer_token('PARENTHESE_FERMANTE')
        corps = self.analyser_bloc()
        return Fonction(nom, params, corps)

    def analyser_retour(self):
        self.consommer_token('RETOURNER')
        valeur = None
        if self.regarder_token().type not in ['POINT_VIRGULE', 'ACCOLADE_FERMANTE']:
            valeur = self.analyser_expression()
        if self.regarder_token().type == 'POINT_VIRGULE':
            self.consommer_token('POINT_VIRGULE')
        return Retour(valeur)

    def analyser_condition(self):
        self.consommer_token('SI')
        self.consommer_token('PARENTHESE_OUVRANTE')
        condition = self.analyser_expression()
        self.consommer_token('PARENTHESE_FERMANTE')
        bloc_si = self.analyser_bloc()
        bloc_sinon = None
        if self.regarder_token().type == 'SINON':
            self.consommer_token('SINON')
            if self.regarder_token().type == 'SI':
                bloc_sinon = Bloc([self.analyser_condition()])
            else:
                bloc_sinon = self.analyser_bloc()
        return Condition(condition, bloc_si, bloc_sinon)

    def analyser_boucle_tant_que(self):
        self.consommer_token('TANT_QUE')
        self.consommer_token('PARENTHESE_OUVRANTE')
        condition = self.analyser_expression()
        self.consommer_token('PARENTHESE_FERMANTE')
        corps = self.analyser_bloc()
        return BoucleTantQue(condition, corps)

    def analyser_bloc(self):
        self.consommer_token('ACCOLADE_OUVRANTE')
        instructions = []
        while self.regarder_token().type != 'ACCOLADE_FERMANTE' and not self.est_a_la_fin():
            instruction = self.analyser_instruction()
            if instruction:
                instructions.append(instruction)
        self.consommer_token('ACCOLADE_FERMANTE')
        return Bloc(instructions)

    def analyser_expression(self):
        return self.analyser_ou()

    def analyser_ou(self):
        gauche = self.analyser_et()
        while self.regarder_token().type == 'OU':
            operateur = self.consommer_token().valeur
            droite = self.analyser_et()
            gauche = ExpressionBinaire(gauche, operateur, droite)
        return gauche

    def analyser_et(self):
        gauche = self.analyser_comparaison()
        while self.regarder_token().type == 'ET':
            operateur = self.consommer_token().valeur
            droite = self.analyser_comparaison()
            gauche = ExpressionBinaire(gauche, operateur, droite)
        return gauche

    def analyser_comparaison(self):
        gauche = self.analyser_terme()
        while self.regarder_token().type in ['EGAL', 'DIFF', 'INF', 'SUP', 'INF_EGAL', 'SUP_EGAL']:
            operateur = self.consommer_token().valeur
            droite = self.analyser_terme()
            gauche = ExpressionBinaire(gauche, operateur, droite)
        return gauche

    def analyser_terme(self):
        gauche = self.analyser_facteur()
        while self.regarder_token().type in ['PLUS', 'MOINS']:
            operateur = self.consommer_token().valeur
            droite = self.analyser_facteur()
            gauche = ExpressionBinaire(gauche, operateur, droite)
        return gauche

    def analyser_facteur(self):
        gauche = self.analyser_unaire()
        while self.regarder_token().type in ['FOIS', 'DIVISE', 'MODULO']:
            operateur = self.consommer_token().valeur
            droite = self.analyser_unaire()
            gauche = ExpressionBinaire(gauche, operateur, droite)
        return gauche

    def analyser_unaire(self):
        if self.regarder_token().type == 'MOINS':
            operateur = self.consommer_token().valeur
            operand = self.analyser_unaire()
            return ExpressionUnaire(operateur, operand)
        return self.analyser_appel()

    def analyser_appel(self):
        gauche = self.analyser_primaire()

        while self.regarder_token().type in ['PARENTHESE_OUVRANTE', 'CROCHET_OUVRANT', 'POINT']:
            if self.regarder_token().type == 'PARENTHESE_OUVRANTE':
                gauche = self.analyser_appel_fonction(gauche)
            elif self.regarder_token().type == 'CROCHET_OUVRANT':
                gauche = self.analyser_acces_crochet(gauche)
            elif self.regarder_token().type == 'POINT':
                # NOUVEAU : Support de l'accès aux attributs (module.fonction)
                gauche = self.analyser_acces_attribut(gauche)
            else:
                break
        return gauche

    def analyser_acces_attribut(self, objet_noeud):
        """
        Analyse l'accès aux attributs : objet.attribut
        """
        self.consommer_token('POINT')
        nom_attribut = self.consommer_token('IDENTIFIANT').valeur
        return AccesAttribut(objet_noeud, nom_attribut)

    def analyser_appel_fonction(self, nom_fonction_noeud):
        self.consommer_token('PARENTHESE_OUVRANTE')
        arguments = []
        if self.regarder_token().type != 'PARENTHESE_FERMANTE':
            arguments.append(self.analyser_expression())
            while self.regarder_token().type == 'VIRGULE':
                self.consommer_token('VIRGULE')
                arguments.append(self.analyser_expression())
        self.consommer_token('PARENTHESE_FERMANTE')
        
        if isinstance(nom_fonction_noeud, Identifiant):
            nom_fonction = nom_fonction_noeud.nom
        else:
            nom_fonction = nom_fonction_noeud
        return AppelFonction(nom_fonction, arguments)

    def analyser_acces_crochet(self, base_noeud):
        self.consommer_token('CROCHET_OUVRANT')
        index_expr = self.analyser_expression()
        self.consommer_token('CROCHET_FERMANT')
        
        if hasattr(index_expr, 'valeur') and isinstance(index_expr.valeur, str):
            return AccesDictionnaire(base_noeud, index_expr)
        else:
            return AccesIndex(base_noeud, index_expr)

    def analyser_primaire(self):
        token = self.regarder_token()
        if token.type == 'NOMBRE':
            self.consommer_token()
            return Littéral(token.valeur)
        elif token.type == 'CHAINE':
            self.consommer_token()
            return Littéral(token.valeur)
        elif token.type == 'VRAI':
            self.consommer_token()
            return Littéral(True)
        elif token.type == 'FAUX':
            self.consommer_token()
            return Littéral(False)
        elif token.type == 'NUL':
            self.consommer_token()
            return Littéral(None)
        elif token.type == 'CROCHET_OUVRANT':
            return self.analyser_liste()
        elif token.type == 'ACCOLADE_OUVRANTE':
            return self.analyser_dictionnaire()
        elif token.type == 'IDENTIFIANT':
            # CHANGEMENT : Accepter TOUS les identifiants (y compris les anciens mots-clés)
            nom = self.consommer_token().valeur
            return Identifiant(nom)
        elif token.type == 'PARENTHESE_OUVRANTE':
            self.consommer_token('PARENTHESE_OUVRANTE')
            expr = self.analyser_expression()
            self.consommer_token('PARENTHESE_FERMANTE')
            return expr
        else:
            raise ParseError(f"Expression inattendue '{token.type}' à la ligne {token.ligne}")

    def analyser_liste(self):
        self.consommer_token()  # '['
        elements = []
        if self.regarder_token().type != 'CROCHET_FERMANT':
            elements.append(self.analyser_expression())
            while self.regarder_token().type == 'VIRGULE':
                self.consommer_token('VIRGULE')
                elements.append(self.analyser_expression())
        self.consommer_token('CROCHET_FERMANT')  # ']'
        
        elements_evalues = []
        for elem in elements:
            if hasattr(elem, 'valeur') and hasattr(elem, 'accepter'):
                elements_evalues.append(elem.valeur)
            else:
                elements_evalues.append(elem)
        
        return Littéral(elements_evalues)

    def analyser_dictionnaire(self):
        self.consommer_token('ACCOLADE_OUVRANTE')  # '{'
        elements = {}
    
        if self.regarder_token().type != 'ACCOLADE_FERMANTE':
            # Premier élément
            cle = self.analyser_expression()
            self.consommer_token('DEUX_POINTS')  # ':'
            valeur = self.analyser_expression()
        
            # CORRECTION : Ne pas évaluer ici, laisser l'interpréteur le faire
            elements[self._extraire_cle_dict(cle)] = valeur
        
            # Éléments suivants
            while self.regarder_token().type == 'VIRGULE':
                self.consommer_token('VIRGULE')
                if self.regarder_token().type == 'ACCOLADE_FERMANTE':
                    break  # Virgule de fin autorisée
            
                cle = self.analyser_expression()
                self.consommer_token('DEUX_POINTS')
                valeur = self.analyser_expression()
            
                elements[self._extraire_cle_dict(cle)] = valeur
    
        self.consommer_token('ACCOLADE_FERMANTE')  # '}'
        # CORRECTION : Retourner un nœud AST spécial pour les dictionnaires
        return DictionnaireLitteral(elements)

    def _extraire_cle_dict(self, noeud_cle):
        """Extrait la clé d'un noeud pour un dictionnaire"""
        if hasattr(noeud_cle, 'valeur'):
            return noeud_cle.valeur
        else:
            return str(noeud_cle)

