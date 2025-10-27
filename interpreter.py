# interpreter.py
from errors import RuntimeError, ReturnException
import builtin
import ia_module
from builtin import _ArretProgramme
from fia_ast import *
from module_resolver import module_resolver

class VisiteurInterpretation:
    def __init__(self):
        # Contextes de variables (pile de dictionnaires)
        self.contextes = [{}]
        
        # Fonctions intégrées
        self.fonctions_integrees = builtin.FONCTIONS_INTEGREES.copy()
        self.fonctions_integrees.update(ia_module.FONCTIONS_IA)
        
        # Fonctions définies par l'utilisateur
        self.fonctions_definies = {}
        
        # === NOUVEAU : SYSTÈME DE MODULES ===
        # Modules importés {alias: contexte_module}
        self.modules_importes = {}
        
        # Fichier courant (pour imports relatifs)
        self.fichier_courant = None
        
        print("🤖 Module IA activé - Fonctions disponibles:")
        for nom_fonction in ia_module.FONCTIONS_IA.keys():
            print(f"   • {nom_fonction}()")

    def executer(self, noeud_ast, fichier_courant=None):
        """Exécute un nœud AST avec contexte de fichier"""
        if fichier_courant:
            ancien_fichier = self.fichier_courant
            self.fichier_courant = fichier_courant
            try:
                return noeud_ast.accepter(self)
            finally:
                self.fichier_courant = ancien_fichier
        else:
            return noeud_ast.accepter(self)

    def executer_fichier(self, chemin_fichier):
        """Exécute un fichier F-IA complet"""
        try:
            # Charger et parser le fichier
            ast_fichier, _ = module_resolver.charger_module(chemin_fichier)
            
            # Exécuter avec le contexte du fichier
            return self.executer(ast_fichier, chemin_fichier)
            
        except Exception as e:
            raise RuntimeError(f"Erreur lors de l'exécution du fichier '{chemin_fichier}': {e}")

    # === MÉTHODES VISITEUR (NOMS CORRECTS) ===

    def visiter_programme(self, programme):
        resultat = None
        try:
            for instruction in programme.instructions:
                resultat = self.executer(instruction)
        except _ArretProgramme:
            return None
        return resultat

    def visiter_bloc(self, bloc):
        nouveau_contexte_cree = False
        if len(self.contextes) == 1:
            self.contextes.append({})
            nouveau_contexte_cree = True
        
        resultat = None
        try:
            for instruction in bloc.instructions:
                resultat = self.executer(instruction)
        finally:
            if nouveau_contexte_cree and len(self.contextes) > 1:
                contexte_bloc = self.contextes.pop()
                if self.contextes:
                    self.contextes[-1].update(contexte_bloc)
        
        return resultat

    def visiter_declarationvariable(self, decl):
        valeur = self.executer(decl.valeur) if decl.valeur else None
        self._set_variable(decl.nom, valeur)

    def visiter_fonction(self, fonction):
        self.fonctions_definies[fonction.nom] = {'params': fonction.parametres, 'corps': fonction.corps}

    def visiter_retour(self, retour):
        valeur = self.executer(retour.valeur) if retour.valeur is not None else None
        raise ReturnException(valeur)

    # === NOUVELLES MÉTHODES POUR LES IMPORTS ===

    def visiter_importmodule(self, import_node):
        """Visite un nœud ImportModule (importer "module.fia" comme alias)"""
        try:
            # Charger le module
            ast_module, contexte_module = module_resolver.charger_module(
            import_node.chemin_module, 
            self.fichier_courant
            )
        
            # Créer un interpréteur dédié pour ce module
            interpreteur_module = VisiteurInterpretation()
            interpreteur_module.fichier_courant = module_resolver.obtenir_chemin_module(
                import_node.chemin_module, 
                self.fichier_courant
            )
        
            # Exécuter le module dans son propre contexte
            interpreteur_module.executer(ast_module)
        
            # CORRECTION : Créer un objet module qui contient variables ET fonctions
            module_obj = {}
        
            # Ajouter les variables du module
            module_obj.update(interpreteur_module.contextes[0])
        
            # IMPORTANT : Ajouter les fonctions comme objets callable
            for nom_func, func_def in interpreteur_module.fonctions_definies.items():
                # Créer une closure qui capture l'interpréteur du module
                def creer_fonction_module(func_definition, interpreteur_parent):
                    def fonction_module(*args):
                        # Utiliser l'interpréteur parent pour exécuter la fonction
                        params = func_definition['params']
                        corps = func_definition['corps']
                    
                        if len(args) != len(params):
                            raise RuntimeError(f"La fonction attend {len(params)} arguments, {len(args)} fournis.")
                    
                        # Créer un contexte local
                        contexte_local = {}
                        for param, arg in zip(params, args):
                            contexte_local[param] = arg
                    
                        # Sauvegarder et remplacer le contexte
                        ancien_contexte = interpreteur_parent.contextes[:]
                        interpreteur_parent.contextes = [interpreteur_parent.contextes[0].copy(), contexte_local]
                    
                        resultat_fonction = None
                        try:
                            resultat_fonction = interpreteur_parent.executer(corps)
                        except ReturnException as e:
                            resultat_fonction = e.value
                        finally:
                            interpreteur_parent.contextes = ancien_contexte
                    
                        return resultat_fonction
                
                    return fonction_module
            
                module_obj[nom_func] = creer_fonction_module(func_def, interpreteur_module)
        
            # Stocker le module avec son alias
            self.modules_importes[import_node.alias] = module_obj
        
            print(f"📦 Module '{import_node.chemin_module}' importé comme '{import_node.alias}'")
        
        except Exception as e:
            raise RuntimeError(f"Erreur lors de l'import du module '{import_node.chemin_module}': {e}")


    def visiter_importdepuis(self, import_depuis_node):
        """Visite un nœud ImportDepuis (depuis "module.fia" importer element1, element2)"""
        try:
            # Charger le module
            ast_module, contexte_module = module_resolver.charger_module(
                import_depuis_node.chemin_module, 
                self.fichier_courant
            )
            
            # Créer un interpréteur dédié pour ce module  
            interpreteur_module = VisiteurInterpretation()
            interpreteur_module.fichier_courant = module_resolver.obtenir_chemin_module(
                import_depuis_node.chemin_module, 
                self.fichier_courant
            )
            
            # Exécuter le module
            interpreteur_module.executer(ast_module)
            
            # Récupérer le contexte du module
            contexte_module = interpreteur_module.contextes[0]
            fonctions_module = interpreteur_module.fonctions_definies
            
            # Importer les éléments demandés dans le contexte courant
            for nom_element, alias_element in import_depuis_node.elements_importes:
                if nom_element in contexte_module:
                    # Variable du module
                    self._set_variable(alias_element, contexte_module[nom_element])
                    print(f"📦 Variable '{nom_element}' importée comme '{alias_element}'")
                elif nom_element in fonctions_module:
                    # Fonction du module
                    self.fonctions_definies[alias_element] = fonctions_module[nom_element]
                    print(f"📦 Fonction '{nom_element}' importée comme '{alias_element}'")
                else:
                    raise RuntimeError(f"'{nom_element}' n'existe pas dans le module '{import_depuis_node.chemin_module}'")
            
        except Exception as e:
            raise RuntimeError(f"Erreur lors de l'import depuis '{import_depuis_node.chemin_module}': {e}")

    # === ASSIGNATIONS ===

    def visiter_assignation(self, assign):
        valeur = self.executer(assign.valeur)
        cible = assign.cible
        if isinstance(cible, Identifiant):
            if not self._variable_existe(cible.nom):
                raise RuntimeError(f"Variable '{cible.nom}' non déclarée avant assignation")
            self._set_variable(cible.nom, valeur)
        elif isinstance(cible, AccesIndex):
            base_list = self.executer(cible.base)
            index_value = self.executer(cible.index)
            if not isinstance(base_list, list):
                raise RuntimeError("L'opérande gauche de l'assignation par index doit être une liste")
            if not isinstance(index_value, int):
                raise RuntimeError("L'index doit être un entier")
            if index_value < 0 or index_value >= len(base_list):
                raise RuntimeError("Index de liste hors limites")
            base_list[index_value] = valeur
        elif isinstance(cible, AccesDictionnaire):
            base_dict = self.executer(cible.base)
            cle_value = self.executer(cible.cle)
            if not isinstance(base_dict, dict):
                raise RuntimeError("L'opérande gauche de l'assignation par clé doit être un dictionnaire")
            base_dict[cle_value] = valeur
        else:
            raise RuntimeError(f"Cible d'assignation invalide")

    def visiter_assignationcomposee(self, assign_composee):
        """Visite une assignation composée (+=, -=, *=, /=, %=)"""
        cible = assign_composee.cible
        
        if isinstance(cible, Identifiant):
            if not self._variable_existe(cible.nom):
                raise RuntimeError(f"Variable '{cible.nom}' non déclarée avant assignation composée")
            
            valeur_actuelle = self._get_variable(cible.nom)
            nouvelle_valeur = self.executer(assign_composee.valeur)
            
            if assign_composee.operateur == '+=':
                if isinstance(valeur_actuelle, str) or isinstance(nouvelle_valeur, str):
                    resultat = str(valeur_actuelle) + str(nouvelle_valeur)
                else:
                    valeur_actuelle = self.convertir_si_nombre(valeur_actuelle)
                    nouvelle_valeur = self.convertir_si_nombre(nouvelle_valeur)
                    resultat = valeur_actuelle + nouvelle_valeur
            elif assign_composee.operateur == '-=':
                valeur_actuelle = self.convertir_si_nombre(valeur_actuelle)
                nouvelle_valeur = self.convertir_si_nombre(nouvelle_valeur)
                resultat = valeur_actuelle - nouvelle_valeur
            elif assign_composee.operateur == '*=':
                valeur_actuelle = self.convertir_si_nombre(valeur_actuelle)
                nouvelle_valeur = self.convertir_si_nombre(nouvelle_valeur)
                resultat = valeur_actuelle * nouvelle_valeur
            elif assign_composee.operateur == '/=':
                valeur_actuelle = self.convertir_si_nombre(valeur_actuelle)
                nouvelle_valeur = self.convertir_si_nombre(nouvelle_valeur)
                if nouvelle_valeur == 0:
                    raise RuntimeError("Division par zéro dans assignation composée")
                resultat = valeur_actuelle / nouvelle_valeur
            elif assign_composee.operateur == '%=':
                valeur_actuelle = self.convertir_si_nombre(valeur_actuelle)
                nouvelle_valeur = self.convertir_si_nombre(nouvelle_valeur)
                resultat = valeur_actuelle % nouvelle_valeur
            else:
                raise RuntimeError(f"Opérateur d'assignation composée inconnu: {assign_composee.operateur}")
            
            self._set_variable(cible.nom, resultat)
            
        else:
            # Gestion des autres types de cibles (listes, dicts) - code similaire à avant
            raise RuntimeError(f"Assignation composée non implémentée pour ce type de cible")

    # === EXPRESSIONS ===

    def visiter_expressionbinaire(self, expr_bin):
        gauche = self.executer(expr_bin.gauche)
        droite = self.executer(expr_bin.droite)

        op = expr_bin.operateur
        
        if op == '+':
            if isinstance(gauche, str) or isinstance(droite, str):
                return str(gauche) + str(droite)
            gauche = self.convertir_si_nombre(gauche)
            droite = self.convertir_si_nombre(droite)
            return gauche + droite
        
        gauche = self.convertir_si_nombre(gauche)
        droite = self.convertir_si_nombre(droite)

        if op == '-': return gauche - droite
        elif op == '*': return gauche * droite
        elif op == '/':
            if droite == 0:
                raise RuntimeError("Division par zéro")
            return gauche / droite
        elif op == '%': return gauche % droite
        elif op == '==': return gauche == droite
        elif op == '!=': return gauche != droite
        elif op == '<': return gauche < droite
        elif op == '<=': return gauche <= droite
        elif op == '>': return gauche > droite
        elif op == '>=': return gauche >= droite
        elif op == 'et': return gauche and droite
        elif op == 'ou': return gauche or droite
        else:
            raise RuntimeError(f"Opérateur binaire inconnu: {op}")

    def visiter_expressionunaire(self, expr_unaire):
        operand_value = self.executer(expr_unaire.operande)
        operand_value = self.convertir_si_nombre(operand_value)
        if expr_unaire.operateur == '-':
            return -operand_value
        elif expr_unaire.operateur == '+':
            return operand_value
        else:
            raise RuntimeError(f"Opérateur unaire non supporté: {expr_unaire.operateur}")

    def visiter_littéral(self, litteral):
        return litteral.valeur

    def visiter_identifiant(self, ident):
        nom = ident.nom
        if nom in self.fonctions_integrees or nom in self.fonctions_definies:
            if nom in self.fonctions_integrees:
                return self.fonctions_integrees[nom]
            elif nom in self.fonctions_definies:
                return self.fonctions_definies[nom]
        else:
            return self._get_variable(nom)

    def visiter_accesattribut(self, acces_node):
        """Visite un AccesAttribut (module.fonction)"""
        if isinstance(acces_node.objet, Identifiant):
            nom_module = acces_node.objet.nom
            if nom_module in self.modules_importes:
                module_proxy = self.modules_importes[nom_module]
                nom_attribut = acces_node.attribut
            
                if nom_attribut in module_proxy:
                    return module_proxy[nom_attribut]
                else:
                    raise RuntimeError(f"'{nom_attribut}' n'existe pas dans le module '{nom_module}'")
            else:
                raise RuntimeError(f"'{nom_module}' n'est pas un module importé")
        else:
            raise RuntimeError("Accès aux attributs supporté uniquement pour les modules")


    def visiter_accesindex(self, acces_index):
        base_value = self.executer(acces_index.base)
        index_value = self.executer(acces_index.index)

        if isinstance(base_value, dict):
            if index_value not in base_value:
                raise RuntimeError(f"Clé '{index_value}' non trouvée dans le dictionnaire")
            return base_value[index_value]

        if not isinstance(base_value, list):
            raise RuntimeError("L'opérande gauche de l'accès par index doit être une liste ou un dictionnaire")
        if not isinstance(index_value, int):
            raise RuntimeError("L'index doit être un entier")
        if index_value < 0 or index_value >= len(base_value):
            raise RuntimeError("Index de liste hors limites")

        element = base_value[index_value]
        if isinstance(element, Noeud):
            return self.executer(element)
        return element

    def visiter_accesdictionnaire(self, acces_dict):
        base_value = self.executer(acces_dict.base)
        cle_value = self.executer(acces_dict.cle)
        
        if not isinstance(base_value, dict):
            raise RuntimeError("L'opérande gauche de l'accès par clé doit être un dictionnaire")
        
        if cle_value not in base_value:
            raise RuntimeError(f"Clé '{cle_value}' non trouvée dans le dictionnaire")
        
        return base_value[cle_value]

    def visiter_appelfonction(self, appel):
        # Gérer les appels de fonctions de modules (module.fonction())
        if isinstance(appel.nom_fonction, AccesAttribut):
            # C'est un appel de type module.fonction()
            fonction_module = self.executer(appel.nom_fonction)
            args = [self.executer(arg) for arg in appel.arguments]
    
            # CORRECTION: Conversion complète des arguments pour les modules ML
            args_convertis = []
            for arg in args:
                if hasattr(arg, 'nom'):  # Si c'est un identifiant (comme un ID de modèle)
                    args_convertis.append(arg.nom)
                elif hasattr(arg, 'valeur'):  # Si c'est un littéral
                    args_convertis.append(self._convertir_en_python(arg.valeur))
                else:
                    args_convertis.append(self._convertir_en_python(arg))
    
            if callable(fonction_module):
                try:
                    return fonction_module(*args_convertis)
                except Exception as e:
                    raise RuntimeError(f"Erreur lors de l'appel de fonction de module: {e}")
            else:
                raise RuntimeError("L'élément n'est pas une fonction")

        # Appel normal
        if isinstance(appel.nom_fonction, str):
            nom_fonction = appel.nom_fonction
        elif hasattr(appel.nom_fonction, 'nom'):
            nom_fonction = appel.nom_fonction.nom
        elif hasattr(appel.nom_fonction, 'valeur'):
            nom_fonction = appel.nom_fonction.valeur
        else:
            nom_fonction = str(appel.nom_fonction)

        args = [self.executer(arg) for arg in appel.arguments]
        args_convertis = [self._convertir_en_python(arg) for arg in args]

        if nom_fonction in self.fonctions_integrees:
            fonction = self.fonctions_integrees[nom_fonction]
            try:
                return fonction(*args_convertis)
            except _ArretProgramme:
                raise _ArretProgramme()
            except TypeError as e:
                raise RuntimeError(f"Erreur lors de l'appel de '{nom_fonction}': {e}")
            except Exception as e:
                raise RuntimeError(f"Erreur IA dans '{nom_fonction}': {str(e)}")
        elif nom_fonction in self.fonctions_definies:
            func_def = self.fonctions_definies[nom_fonction]
            params = func_def['params']
            corps = func_def['corps']
            if len(args) != len(params):
                raise RuntimeError(f"La fonction '{nom_fonction}' attend {len(params)} arguments, {len(args)} fournis.")
            
            contexte_local = {}
            for param, arg in zip(params, args):
                contexte_local[param] = arg
            
            ancien_contexte = self.contextes[:]
            self.contextes = [ancien_contexte[0].copy(), contexte_local]
            resultat_fonction = None
            try:
                resultat_fonction = self.executer(corps)
            except ReturnException as e:
                resultat_fonction = e.value
            finally:
                self.contextes = ancien_contexte
            return resultat_fonction
        else:
            raise RuntimeError(f"Fonction '{nom_fonction}' non définie")

    # === STRUCTURES DE CONTRÔLE ===

    def visiter_condition(self, condition):
        valeur_condition = self.executer(condition.condition)
        if valeur_condition:
            self.executer(condition.bloc_si)
        elif condition.bloc_sinon:
            self.executer(condition.bloc_sinon)

    def visiter_boucletantque(self, boucle):
        condition_value = self.executer(boucle.condition)
        compteur = 0
        while condition_value and compteur < 1000:  # AUGMENTÉ À 1000
            self.executer(boucle.corps)
            condition_value = self.executer(boucle.condition)
            compteur += 1
        if compteur >= 1000:
            print("🛑 Sécurité: boucle arrêtée après 1000 itérations")

    def visiter_bouclepour(self, boucle):
        self.executer(boucle.init)
        condition_value = self.executer(boucle.condition)
        compteur = 0
        while condition_value and compteur < 1000:  # AUGMENTÉ À 1000
            self.executer(boucle.corps)
            self.executer(boucle.increment)
            condition_value = self.executer(boucle.condition)
            compteur += 1
        if compteur >= 1000:
            print("🛑 Sécurité: boucle arrêtée après 1000 itérations")

    def visiter_bouclepourdans(self, boucle):
        """Visite une boucle pour...dans"""
        iterable_value = self.executer(boucle.iterable)
        
        if not isinstance(iterable_value, (list, dict, str)):
            raise RuntimeError("L'objet à droite de 'dans' doit être itérable (liste, dictionnaire ou chaîne)")
        
        self.contextes.append({})
        
        compteur = 0
        try:
            if isinstance(iterable_value, list):
                for element in iterable_value:
                    if compteur >= 1000:  # AUGMENTÉ À 1000
                        print("🛑 Sécurité: boucle pour...dans arrêtée après 1000 itérations")
                        break
                    self._set_variable(boucle.variable, element)
                    self.executer(boucle.corps)
                    compteur += 1
            elif isinstance(iterable_value, dict):
                for cle in iterable_value.keys():
                    if compteur >= 1000:  # AUGMENTÉ À 1000
                        print("🛑 Sécurité: boucle pour...dans arrêtée après 1000 itérations")
                        break
                    self._set_variable(boucle.variable, cle)
                    self.executer(boucle.corps)
                    compteur += 1
            elif isinstance(iterable_value, str):
                for caractere in iterable_value:
                    if compteur >= 1000:  # AUGMENTÉ À 1000
                        print("🛑 Sécurité: boucle pour...dans arrêtée après 1000 itérations")
                        break
                    self._set_variable(boucle.variable, caractere)
                    self.executer(boucle.corps)
                    compteur += 1
        finally:
            if len(self.contextes) > 1:
                self.contextes.pop()

    def visiter_dictionnairelitteral(self, dict_node):
        """Visite un dictionnaire littéral en évaluant toutes les valeurs"""
        elements_evalues = {}
        for cle, valeur_noeud in dict_node.elements.items():
            # Évaluer chaque valeur du dictionnaire
            valeur_evaluee = self.executer(valeur_noeud)
            elements_evalues[cle] = valeur_evaluee
        return elements_evalues


    # === UTILITAIRE ===

    def visiter_expressionstatement(self, stmt):
        return self.executer(stmt.expression)

    # === MÉTHODES UTILITAIRES ===

    def _get_variable(self, nom):
        """Recherche une variable dans la pile des contextes."""
        for contexte in reversed(self.contextes):
            if nom in contexte:
                return contexte[nom]
        raise RuntimeError(f"Variable '{nom}' non définie")

    def _variable_existe(self, nom):
        """Vérifie si une variable existe dans la pile des contextes."""
        for contexte in reversed(self.contextes):
            if nom in contexte:
                return True
        return False

    def _set_variable(self, nom, valeur):
        """Définit une variable dans le contexte local actuel."""
        if self.contextes:
            self.contextes[-1][nom] = valeur
        else:
            self.contextes = [{}]
            self.contextes[0][nom] = valeur

    def convertir_si_nombre(self, valeur):
        """Convertit une valeur en nombre si possible"""
        if isinstance(valeur, str):
            if valeur.replace('.', '').replace('-', '').isdigit():
                return float(valeur) if '.' in valeur else int(valeur)
        return valeur

    def _convertir_en_python(self, valeur):
        """Convertit récursivement les objets F-IA en types Python natifs."""
        from fia_ast import Littéral, Identifiant
    
        # CORRECTION: Gestion des identifiants F-IA
        if isinstance(valeur, Identifiant):
            # Si c'est un identifiant, récupérer sa valeur dans le contexte
            return self._get_variable(valeur.nom)
        elif isinstance(valeur, Littéral):
            return self._convertir_en_python(valeur.valeur)
        elif isinstance(valeur, list):
            return [self._convertir_en_python(item) for item in valeur]
        elif isinstance(valeur, dict):
            return {k: self._convertir_en_python(v) for k, v in valeur.items()}
        else:
            return valeur
