# builtin.py
import json
import math
import random
from errors import RuntimeError

def _imprimer(*args):
    # Supporte l'affichage de plusieurs arguments comme print
    print(*args)

def _longueur(obj):
    try:
        return len(obj)
    except Exception:
        raise RuntimeError("Erreur d'exécution: 'longueur' attend une liste, chaîne ou dictionnaire")

def _arrondir(nombre, decimales=0):
    try:
        # Conversion sûre des arguments
        nombre_float = float(nombre)
        decimales_int = int(decimales) if decimales is not None else 0
        return round(nombre_float, decimales_int)
    except Exception as e:
        raise RuntimeError(f"Erreur d'exécution: 'arrondir' attend (nombre, [décimales optionnel]) - {e}")


def _aleatoire():
    import random
    return random.random()

def _racine(nombre):
    import math
    try:
        return math.sqrt(float(nombre))
    except Exception:
        raise RuntimeError("Erreur d'exécution: 'racine' attend un nombre")

def _puissance(base, exposant):
    try:
        return float(base) ** float(exposant)
    except Exception:
        raise RuntimeError("Erreur d'exécution: 'puissance' attend (base, exposant)")

# ========== CONVERSIONS ROBUSTES (NOUVELLES) ==========

def _entier(val):
    """Conversion robuste vers entier avec gestion d'erreurs explicites"""
    # None -> 0
    if val is None:
        return 0
    # Bool -> 1/0
    if isinstance(val, bool):
        return 1 if val else 0
    # Int -> identique
    if isinstance(val, int):
        return val
    # Float -> tronqué vers 0 (comme int())
    if isinstance(val, float):
        return int(val)
    # Str -> parsing tolerant
    if isinstance(val, str):
        s = val.strip()
        if s == "":
            return 0
        # Essayer int direct
        try:
            return int(s)
        except ValueError:
            # Essayer float puis tronquer
            try:
                return int(float(s))
            except ValueError:
                raise RuntimeError(f"Conversion invalide: entier('{val}')")
    # List/Dict -> erreur
    if isinstance(val, (list, dict)):
        raise RuntimeError("Conversion invalide: entier() ne supporte pas les listes ou dictionnaires")
    # Fallback Python
    try:
        return int(val)
    except Exception:
        raise RuntimeError(f"Conversion invalide: entier({val})")

def _decimal(val):
    """Conversion robuste vers nombre décimal (float)"""
    if val is None:
        return 0.0
    if isinstance(val, bool):
        return 1.0 if val else 0.0
    if isinstance(val, (int, float)):
        return float(val)
    if isinstance(val, str):
        s = val.strip()
        if s == "":
            return 0.0
        try:
            return float(s)
        except ValueError:
            raise RuntimeError(f"Conversion invalide: decimal('{val}')")
    if isinstance(val, (list, dict)):
        raise RuntimeError("Conversion invalide: decimal() ne supporte pas les listes ou dictionnaires")
    try:
        return float(val)
    except Exception:
        raise RuntimeError(f"Conversion invalide: decimal({val})")

def _chaine(val):
    """Conversion robuste vers chaîne avec format cohérent"""
    # Pour list/dict, format JSON compact pour cohérence
    if isinstance(val, (list, dict)):
        try:
            return json.dumps(val, ensure_ascii=False, separators=(',', ':'))
        except Exception:
            return str(val)
    if val is None:
        return ""
    return str(val)

def _booleen(val):
    """Conversion robuste vers booléen avec règles explicites"""
    if val is None:
        return False
    if isinstance(val, bool):
        return val
    if isinstance(val, (int, float)):
        return val != 0
    if isinstance(val, str):
        s = val.strip().lower()
        if s in ["true", "vrai", "oui", "1"]:
            return True
        if s in ["false", "faux", "non", "0", ""]:
            return False
        return True  # toute autre chaîne non vide -> True
    if isinstance(val, (list, dict)):
        return len(val) > 0
    return True

# ========== FONCTIONS EXISTANTES ==========

# Dictionnaires
def _cles(d):
    if not isinstance(d, dict):
        raise RuntimeError("Erreur d'exécution: 'cles' attend un dictionnaire")
    return list(d.keys())

def _valeurs(d):
    if not isinstance(d, dict):
        raise RuntimeError("Erreur d'exécution: 'valeurs' attend un dictionnaire")
    return list(d.values())

def _contient_cle(d, cle):
    if not isinstance(d, dict):
        raise RuntimeError("Erreur d'exécution: 'contient_cle' attend un dictionnaire")
    return cle in d

def _supprimer_cle(d, cle):
    if not isinstance(d, dict):
        raise RuntimeError("Erreur d'exécution: 'supprimer_cle' attend un dictionnaire")
    d.pop(cle, None)
    return d

def _fusionner(d1, d2):
    if not isinstance(d1, dict) or not isinstance(d2, dict):
        raise RuntimeError("Erreur d'exécution: 'fusionner' attend deux dictionnaires")
    r = d1.copy()
    r.update(d2)
    return r

def _vider(d):
    if not isinstance(d, dict):
        raise RuntimeError("Erreur d'exécution: 'vider' attend un dictionnaire")
    d.clear()
    return d

# Listes
def _ajouter(l, e):
    if not isinstance(l, list):
        raise RuntimeError("Erreur d'exécution: 'ajouter' attend une liste")
    l.append(e)
    return l  # IMPORTANT: Retourner la liste

def _retirer(l, index):
    if not isinstance(l, list):
        raise RuntimeError("Erreur d'exécution: 'retirer' attend une liste")
    if not isinstance(index, int) or index < 0 or index >= len(l):
        raise RuntimeError("Erreur d'exécution: index invalide dans 'retirer'")
    l.pop(index)
    return l  # IMPORTANT: Retourner la liste


def _trier(l):
    if not isinstance(l, list):
        raise RuntimeError("Erreur d'exécution: 'trier' attend une liste")
    try:
        l.sort()
    except Exception:
        raise RuntimeError("Erreur d'exécution: la liste ne peut pas être triée")
    return l

def _inverser(l):
    if not isinstance(l, list):
        raise RuntimeError("Erreur d'exécution: 'inverser' attend une liste")
    l.reverse()
    return l

def _copier(l):
    if not isinstance(l, list):
        raise RuntimeError("Erreur d'exécution: 'copier' attend une liste")
    return l.copy()

def _contient(l, e):
    if not isinstance(l, list):
        raise RuntimeError("Erreur d'exécution: 'contient' attend une liste")
    return e in l

def _index_de(l, e):
    if not isinstance(l, list):
        raise RuntimeError("Erreur d'exécution: 'index_de' attend une liste")
    try:
        return l.index(e)
    except ValueError:
        return -1

def _compter(l, e):
    if not isinstance(l, list):
        raise RuntimeError("Erreur d'exécution: 'compter' attend une liste")
    return l.count(e)

# Chaînes
def _majuscule(t):
    if not isinstance(t, str):
        raise RuntimeError("Erreur d'exécution: 'majuscule' attend une chaîne")
    return t.upper()

def _minuscule(t):
    if not isinstance(t, str):
        raise RuntimeError("Erreur d'exécution: 'minuscule' attend une chaîne")
    return t.lower()

def _remplacer(t, ancien, nouveau):
    if not isinstance(t, str):
        raise RuntimeError("Erreur d'exécution: 'remplacer' attend une chaîne")
    return t.replace(str(ancien), str(nouveau))

def _diviser(t, sep):
    if not isinstance(t, str):
        raise RuntimeError("Erreur d'exécution: 'diviser' attend une chaîne")
    return t.split(str(sep))

def _joindre(l, sep):
    if not isinstance(l, list):
        raise RuntimeError("Erreur d'exécution: 'joindre' attend une liste")
    return str(sep).join(str(x) for x in l)

# I/O utilisateur
def _lire():
    try:
        return input()
    except EOFError:
        return ""
    except Exception as e:
        raise RuntimeError(f"Erreur d'exécution: 'lire' a échoué: {e}")

# Arrêt contrôlé
class _ArretProgramme(Exception):
    pass

def _arreter():
    # Cette fonction peut être interceptée par l'interpréteur si besoin
    raise _ArretProgramme()

# === NOUVELLES FONCTIONS IA ===
# Import avec gestion d'erreur pour les dépendances IA
def _safe_import_ai():
    """Import sécurisé du module IA"""
    try:
        from ai_integration import (
            _appeler_ia, _lister_plateformes_ia, _lister_modeles_ia, 
            _generer_reponse_bot, _verifier_config_ia
        )
        return {
            'appeler_ia': _appeler_ia,
            'lister_plateformes_ia': _lister_plateformes_ia,
            'lister_modeles_ia': _lister_modeles_ia,
            'generer_reponse_bot': _generer_reponse_bot,
            'verifier_config_ia': _verifier_config_ia
        }
    except ImportError as e:
        # Si les dépendances IA ne sont pas installées
        def _ia_non_disponible(*args, **kwargs):
            raise RuntimeError("Fonctions IA non disponibles. Installez les dépendances: pip install -r requirements.txt")
        
        return {
            'appeler_ia': _ia_non_disponible,
            'lister_plateformes_ia': _ia_non_disponible,
            'lister_modeles_ia': _ia_non_disponible,
            'generer_reponse_bot': _ia_non_disponible,
            'verifier_config_ia': _ia_non_disponible
        }
    except Exception as e:
        # Autres erreurs (clés API manquantes, etc.)
        def _ia_erreur(*args, **kwargs):
            raise RuntimeError(f"Erreur IA: {str(e)}")
        
        return {
            'appeler_ia': _ia_erreur,
            'lister_plateformes_ia': _ia_erreur,
            'lister_modeles_ia': _ia_erreur,
            'generer_reponse_bot': _ia_erreur,
            'verifier_config_ia': _ia_erreur
        }

# Charger les fonctions IA
_ai_functions = _safe_import_ai()

# === INTERFACE MACHINE LEARNING ===
def _appeler_python_ml(nom_fonction, args):
    """Interface entre F-IA et le backend ML Python"""
    try:
        from ml_backend import _appeler_python_ml
        return _appeler_python_ml(nom_fonction, args)
    except ImportError:
        raise RuntimeError("Backend ML non disponible. Vérifiez l'installation des dépendances.")
    except Exception as e:
        raise RuntimeError(f"Erreur ML: {e}")

# Table des fonctions intégrées exposées au langage F-IA
FONCTIONS_INTEGREES = {
    # Fonctions de base
    "imprimer": _imprimer,
    "longueur": _longueur,
    "arrondir": _arrondir,
    "aleatoire": _aleatoire,
    "racine": _racine,
    "puissance": _puissance,
    
    # Conversions robustes (NOUVELLES)
    "entier": _entier,
    "decimal": _decimal,
    "chaine": _chaine,
    "booleen": _booleen,

    # Dictionnaires
    "cles": _cles,
    "valeurs": _valeurs,
    "contient_cle": _contient_cle,
    "supprimer_cle": _supprimer_cle,
    "fusionner": _fusionner,
    "vider": _vider,

    # Listes
    "ajouter": _ajouter,
    "retirer": _retirer,
    "trier": _trier,
    "inverser": _inverser,
    "copier": _copier,
    "contient": _contient,
    "index_de": _index_de,
    "compter": _compter,

    # Chaînes
    "majuscule": _majuscule,
    "minuscule": _minuscule,
    "remplacer": _remplacer,
    "diviser": _diviser,
    "joindre": _joindre,

    # I/O utilisateur
    "lire": _lire,
    "arreter": _arreter,

    # === INTERFACE MACHINE LEARNING ===
    "appeler_python_ml": _appeler_python_ml,

    # === FONCTIONS IA INTÉGRÉES ===
    "appeler_ia": _ai_functions['appeler_ia'],
    "lister_plateformes_ia": _ai_functions['lister_plateformes_ia'],
    "lister_modeles_ia": _ai_functions['lister_modeles_ia'],
    "generer_reponse_bot": _ai_functions['generer_reponse_bot'],
    "verifier_config_ia": _ai_functions['verifier_config_ia'],
}
