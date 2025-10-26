# module_resolver.py
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set
from errors import RuntimeError

class ModuleResolver:
    """Gestionnaire de résolution et cache des modules F-IA"""
    
    def __init__(self):
        # Cache des modules déjà chargés {chemin_absolu: ast_module}
        self.cache_modules: Dict[str, any] = {}
        
        # Cache des contextes d'exécution {chemin_absolu: contexte}
        self.cache_contextes: Dict[str, dict] = {}
        
        # Stack des modules en cours de chargement (détection cycles)
        self.stack_chargement: Set[str] = set()
        
        # Chemins de recherche des modules
        self.chemins_recherche: List[Path] = []
        self._initialiser_chemins()
    
    def _initialiser_chemins(self):
        """Initialise les chemins de recherche des modules"""
        # 1. Répertoire courant
        self.chemins_recherche.append(Path.cwd())
        
        # 2. Répertoire ./lib (bibliothèques locales)
        lib_path = Path.cwd() / "lib"
        if lib_path.exists():
            self.chemins_recherche.append(lib_path)
        
        # 3. Variable d'environnement FIA_PATH
        fia_path = os.getenv("FIA_PATH")
        if fia_path:
            for chemin in fia_path.split(os.pathsep):
                path_obj = Path(chemin)
                if path_obj.exists():
                    self.chemins_recherche.append(path_obj)
        
        # 4. Répertoire d'installation de F-IA (futur)
        # TODO: Ajouter ~/.fia/modules/ quand installé globalement
    
    def resoudre_chemin(self, nom_module: str, fichier_courant: Optional[str] = None) -> Optional[Path]:
        """
        Résout le chemin d'un module selon les règles de F-IA
        
        Args:
            nom_module: Nom du module (ex: "utils/math.fia", "collections.fia")
            fichier_courant: Chemin du fichier qui fait l'import (pour imports relatifs)
        
        Returns:
            Path absolu du module ou None si non trouvé
        """
        # Normaliser le nom (remplacer \ par / sur Windows)
        nom_module = nom_module.replace("\\", "/")
        
        # Si pas d'extension, ajouter .fia
        if not nom_module.endswith('.fia'):
            nom_module += '.fia'
        
        chemins_a_tester = []
        
        # 1. Si import relatif et fichier_courant fourni
        if fichier_courant and nom_module.startswith('./'):
            rep_courant = Path(fichier_courant).parent
            chemin_relatif = rep_courant / nom_module[2:]  # Enlever ./
            chemins_a_tester.append(chemin_relatif)
        
        # 2. Chemins absolus dans tous les répertoires de recherche
        if not nom_module.startswith('./'):
            for repertoire in self.chemins_recherche:
                chemin_complet = repertoire / nom_module
                chemins_a_tester.append(chemin_complet)
        
        # 3. Tester chaque chemin
        for chemin in chemins_a_tester:
            if chemin.exists() and chemin.is_file():
                return chemin.resolve()  # Chemin absolu
        
        return None
    
    def charger_module(self, nom_module: str, fichier_courant: Optional[str] = None):
        """
        Charge un module F-IA avec gestion du cache et des cycles
        
        Args:
            nom_module: Nom du module à charger
            fichier_courant: Fichier qui demande le chargement
        
        Returns:
            (ast_module, contexte_execution)
        
        Raises:
            RuntimeError: Si module non trouvé ou dépendance circulaire
        """
        # 1. Résoudre le chemin
        chemin_module = self.resoudre_chemin(nom_module, fichier_courant)
        if not chemin_module:
            # Construire un message d'erreur détaillé
            chemins_testes = []
            if fichier_courant and nom_module.startswith('./'):
                rep_courant = Path(fichier_courant).parent
                chemins_testes.append(str(rep_courant / nom_module[2:]))
            else:
                for rep in self.chemins_recherche:
                    chemins_testes.append(str(rep / nom_module))
            
            raise RuntimeError(
                f"Module '{nom_module}' non trouvé.\n"
                f"Chemins testés :\n" + 
                "\n".join(f"  - {c}" for c in chemins_testes)
            )
        
        chemin_str = str(chemin_module)
        
        # 2. Vérifier le cache
        if chemin_str in self.cache_modules:
            return self.cache_modules[chemin_str], self.cache_contextes[chemin_str]
        
        # 3. Détecter les dépendances circulaires
        if chemin_str in self.stack_chargement:
            cycle = " → ".join(self.stack_chargement) + f" → {nom_module}"
            raise RuntimeError(f"Dépendance circulaire détectée : {cycle}")
        
        # 4. Charger et parser le module
        try:
            self.stack_chargement.add(chemin_str)
            
            # Lire le contenu
            with open(chemin_module, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            # Parser le module (imports nécessaires)
            from lexer import LexerFIA
            from parser import ParserFIA
            
            lexer = LexerFIA(contenu)
            tokens = lexer.tokeniser()
            parser = ParserFIA(tokens)
            ast_module = parser.analyser()
            
            # Mettre en cache
            self.cache_modules[chemin_str] = ast_module
            self.cache_contextes[chemin_str] = {}  # Contexte vide initialement
            
            return ast_module, self.cache_contextes[chemin_str]
            
        except Exception as e:
            raise RuntimeError(f"Erreur lors du chargement du module '{nom_module}': {e}")
        finally:
            # Retirer de la pile de chargement
            self.stack_chargement.discard(chemin_str)
    
    def obtenir_chemin_module(self, nom_module: str, fichier_courant: Optional[str] = None) -> str:
        """Obtient le chemin absolu d'un module (pour le cache)"""
        chemin = self.resoudre_chemin(nom_module, fichier_courant)
        return str(chemin) if chemin else ""
    
    def vider_cache(self):
        """Vide le cache des modules (utile pour le développement/tests)"""
        self.cache_modules.clear()
        self.cache_contextes.clear()
    
    def lister_modules_charges(self) -> List[str]:
        """Liste les modules actuellement en cache"""
        return list(self.cache_modules.keys())

# Instance globale du resolver (singleton)
module_resolver = ModuleResolver()
