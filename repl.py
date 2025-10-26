# repl.py
import sys
from lexer import LexerFIA
from parser import ParserFIA
from interpreter import VisiteurInterpretation
from errors import RuntimeError, LexerError, ParseError

class ReplFIA:
    def __init__(self):
        self.interpreter = VisiteurInterpretation()
        self.historique = []
        
    def evaluer_ligne(self, ligne):
        """Évalue une ligne de code F-IA"""
        try:
            # Ajouter à l'historique
            self.historique.append(ligne)
            
            # Lexer
            lexer = LexerFIA(ligne)
            tokens = lexer.tokeniser()
            
            # Parser
            parser = ParserFIA(tokens)
            ast = parser.analyser()
            
            # Exécuter
            resultat = self.interpreter.executer(ast)
            
            # Afficher le résultat si ce n'est pas None
            if resultat is not None:
                print(f"=> {resultat}")
                
        except LexerError as e:
            print(f"❌ Erreur lexicale: {e}")
        except ParseError as e:
            print(f"❌ Erreur de syntaxe: {e}")
        except RuntimeError as e:
            print(f"❌ Erreur d'exécution: {e}")
        except Exception as e:
            print(f"❌ Erreur inattendue: {e}")
    
    def afficher_aide(self):
        """Affiche l'aide du REPL"""
        print("🤖 === AIDE F-IA REPL ===")
        print("Commandes spéciales:")
        print("  aide()          - Afficher cette aide")
        print("  quitter()       - Quitter le REPL")
        print("  historique()    - Voir l'historique des commandes")
        print("  vider()         - Vider l'historique")
        print("  variables()     - Voir les variables définies")
        print()
        print("🆕 Système de modules:")
        print('  importer "lib/math.fia" comme math')
        print('  depuis "lib/collections.fia" importer pile')
        print('  math.carre(5)')
        print()
        print("📝 Exemples de base:")
        print("  soit x = 10")
        print("  imprimer('Bonjour F-IA!')")
        print("  pour i dans [1, 2, 3] { imprimer(i) }")
    
    def afficher_historique(self):
        """Affiche l'historique des commandes"""
        print("📜 Historique des commandes:")
        for i, cmd in enumerate(self.historique, 1):
            print(f"  {i}. {cmd}")
    
    def vider_historique(self):
        """Vide l'historique"""
        self.historique.clear()
        print("🗑️ Historique vidé")
    
    def afficher_variables(self):
        """Affiche les variables définies"""
        if self.interpreter.contextes and self.interpreter.contextes[0]:
            print("📦 Variables définies:")
            for nom, valeur in self.interpreter.contextes[0].items():
                print(f"  {nom} = {repr(valeur)}")
        else:
            print("📦 Aucune variable définie")
        
        if self.interpreter.modules_importes:
            print("📚 Modules importés:")
            for nom_module in self.interpreter.modules_importes.keys():
                print(f"  {nom_module}")

def demarrer_repl():
    """Démarre le REPL F-IA"""
    repl = ReplFIA()
    
    print("🚀 F-IA REPL - Mode Interactif")
    print("💡 Tapez 'aide()' pour l'aide ou 'quitter()' pour sortir")
    print("🆕 Support complet des modules!")
    print()
    
    try:
        while True:
            try:
                # Lire l'entrée utilisateur
                ligne = input("f-ia> ").strip()
                
                # Commandes spéciales
                if ligne == "aide()":
                    repl.afficher_aide()
                elif ligne == "quitter()":
                    print("👋 Au revoir !")
                    break
                elif ligne == "historique()":
                    repl.afficher_historique()
                elif ligne == "vider()":
                    repl.vider_historique()
                elif ligne == "variables()":
                    repl.afficher_variables()
                elif ligne == "":
                    continue  # Ligne vide
                else:
                    # Évaluer la ligne
                    repl.evaluer_ligne(ligne)
                    
            except KeyboardInterrupt:
                print("\n💡 Utilisez 'quitter()' pour sortir proprement")
            except EOFError:
                print("\n👋 Au revoir !")
                break
                
    except Exception as e:
        print(f"❌ Erreur fatale du REPL: {e}")

if __name__ == "__main__":
    demarrer_repl()
