# fia_ast.py
"""
Nœuds de l'Arbre Syntaxique Abstrait (AST) pour le langage F-IA
"""

class Noeud:
    """Classe de base pour tous les nœuds de l'AST"""
    def accepter(self, visiteur):
        nom_methode = 'visiter_' + type(self).__name__.lower()
        methode = getattr(visiteur, nom_methode, None)
        if methode:
            return methode(self)
        else:
            raise NotImplementedError(f"Méthode {nom_methode} non implémentée dans le visiteur")

# === NŒUDS STRUCTURELS ===

class Programme(Noeud):
    def __init__(self, instructions):
        self.instructions = instructions

class Bloc(Noeud):
    def __init__(self, instructions):
        self.instructions = instructions

# === NŒUDS DE DÉCLARATION ET DÉFINITION ===

class DeclarationVariable(Noeud):
    def __init__(self, nom, valeur=None, type_declare=None):
        self.nom = nom
        self.valeur = valeur
        self.type_declare = type_declare  # Pour le futur système de types

class Fonction(Noeud):
    def __init__(self, nom, parametres, corps, type_retour=None):
        self.nom = nom
        self.parametres = parametres
        self.corps = corps
        self.type_retour = type_retour  # Pour le futur système de types

class Retour(Noeud):
    def __init__(self, valeur=None):
        self.valeur = valeur

# === NOUVEAUX NŒUDS POUR LES IMPORTS ===

class ImportModule(Noeud):
    """
    Nœud pour : importer "chemin/module.fia" comme alias
    """
    def __init__(self, chemin_module, alias=None):
        self.chemin_module = chemin_module
        self.alias = alias or self._extraire_nom_defaut(chemin_module)
    
    def _extraire_nom_defaut(self, chemin):
        """Extrait le nom par défaut d'un chemin de module"""
        # "utils/math.fia" -> "math"
        # "collections.fia" -> "collections"
        nom_fichier = chemin.split('/')[-1]  # Prendre la dernière partie
        return nom_fichier.replace('.fia', '') if nom_fichier.endswith('.fia') else nom_fichier

class ImportDepuis(Noeud):
    """
    Nœud pour : depuis "module.fia" importer fonction1, fonction2 comme alias2
    """
    def __init__(self, chemin_module, elements_importes):
        self.chemin_module = chemin_module
        self.elements_importes = elements_importes  # Liste de (nom, alias)

# === NŒUDS D'ASSIGNATION ===

class Assignation(Noeud):
    def __init__(self, cible, valeur):
        self.cible = cible
        self.valeur = valeur

class AssignationComposee(Noeud):
    def __init__(self, cible, operateur, valeur):
        self.cible = cible
        self.operateur = operateur  # +=, -=, *=, /=, %=
        self.valeur = valeur

# === NŒUDS D'EXPRESSIONS ===

class ExpressionBinaire(Noeud):
    def __init__(self, gauche, operateur, droite):
        self.gauche = gauche
        self.operateur = operateur
        self.droite = droite

class ExpressionUnaire(Noeud):
    def __init__(self, operateur, operande):
        self.operateur = operateur
        self.operande = operande

class Littéral(Noeud):
    def __init__(self, valeur):
        self.valeur = valeur

class Identifiant(Noeud):
    def __init__(self, nom):
        self.nom = nom

class AccesAttribut(Noeud):
    """
    Nouveau nœud pour l'accès aux attributs de modules
    Ex: math.racine_carree()
    """
    def __init__(self, objet, attribut):
        self.objet = objet      # Identifiant du module
        self.attribut = attribut # Nom de l'attribut/fonction

class AccesIndex(Noeud):
    def __init__(self, base, index):
        self.base = base
        self.index = index

class AccesDictionnaire(Noeud):
    def __init__(self, base, cle):
        self.base = base
        self.cle = cle

class AppelFonction(Noeud):
    def __init__(self, nom_fonction, arguments):
        self.nom_fonction = nom_fonction
        self.arguments = arguments

# === NŒUDS DE CONTRÔLE DE FLUX ===

class Condition(Noeud):
    def __init__(self, condition, bloc_si, bloc_sinon=None):
        self.condition = condition
        self.bloc_si = bloc_si
        self.bloc_sinon = bloc_sinon

class BoucleTantQue(Noeud):
    def __init__(self, condition, corps):
        self.condition = condition
        self.corps = corps

class BouclePour(Noeud):
    def __init__(self, init, condition, increment, corps):
        self.init = init
        self.condition = condition
        self.increment = increment
        self.corps = corps

class BouclePourDans(Noeud):
    def __init__(self, variable, iterable, corps):
        self.variable = variable
        self.iterable = iterable
        self.corps = corps

# === NŒUD UTILITAIRE ===

class ExpressionStatement(Noeud):
    """Wrapper pour les expressions utilisées comme instructions"""
    def __init__(self, expression):
        self.expression = expression

class DictionnaireLitteral(Noeud):
    """Nœud spécial pour les dictionnaires littéraux"""
    def __init__(self, elements):
        self.elements = elements  # {clé_str: noeud_valeur}
