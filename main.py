# main.py
import sys
import os
from pathlib import Path
from lexer import LexerFIA
from parser import ParserFIA
from interpreter import VisiteurInterpretation
from errors import RuntimeError, LexerError, ParseError
from repl import demarrer_repl

def executer_fichier(chemin_fichier):
    """Exécute un fichier F-IA"""
    try:
        # Vérifier que le fichier existe
        if not Path(chemin_fichier).exists():
            print(f"❌ Erreur: Fichier '{chemin_fichier}' non trouvé")
            return 1
        
        # Lire le contenu
        with open(chemin_fichier, 'r', encoding='utf-8') as f:
            contenu = f.read()
        
        # Lexer
        lexer = LexerFIA(contenu)
        tokens = lexer.tokeniser()
        
        # Parser
        parser = ParserFIA(tokens)
        ast = parser.analyser()
        
        # Interpréteur
        interpreter = VisiteurInterpretation()
        
        # Exécuter avec contexte de fichier
        interpreter.executer(ast, chemin_fichier)
        
        return 0
        
    except LexerError as e:
        print(f"❌ Erreur lexicale: {e}")
        return 1
    except ParseError as e:
        print(f"❌ Erreur de syntaxe: {e}")
        return 1
    except RuntimeError as e:
        print(f"❌ Erreur d'exécution: {e}")
        return 1
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return 1

def afficher_aide():
    """Affiche l'aide du programme"""
    print("🚀 F-IA - Langage de Programmation Français avec IA")
    print()
    print("Usage:")
    print("  python main.py                    # Mode interactif (REPL)")
    print("  python main.py <fichier.fia>      # Exécuter un fichier")
    print("  python main.py --aide             # Afficher cette aide")
    print()
    print("Exemples:")
    print("  python main.py exemples/test_modules.fia")
    print("  python main.py exemples/chatbot_simple.fia")
    print(" python main.py exemples/test_ml_basic.fia")
    print(" python main.py exemples/test_csv_ml.fia")
    print(" python main.py exemples/demo_ml_complet.fia")
    print()
    print("🆕 Nouveau système de modules:")
    print('  importer "lib/math.fia" comme math')
    print('  depuis "collections.fia" importer pile')
    print()
    print("Documentation: https://github.com/Jimmyjoe13/f-ia-2")

def main():
    """Point d'entrée principal"""
    print("🤖 F-IA v2.0 - Phase 3 ML native activée")
    
    # Pas d'arguments = mode REPL
    if len(sys.argv) == 1:
        print("🔄 Démarrage du mode interactif...")
        print("💡 Tapez 'aide()' pour l'aide ou Ctrl+C pour quitter")
        demarrer_repl()
        return 0
    
    # Aide
    if sys.argv[1] in ['--aide', '--help', '-h']:
        afficher_aide()
        return 0
    
    # Exécution de fichier
    fichier = sys.argv[1]
    if not fichier.endswith('.fia'):
        print("⚠️  Attention: Les fichiers F-IA ont généralement l'extension .fia")
    
    print(f"📂 Exécution du fichier: {fichier}")
    return executer_fichier(fichier)

if __name__ == "__main__":
    try:
        code_sortie = main()
        sys.exit(code_sortie)
    except KeyboardInterrupt:
        print("\n👋 Au revoir !")
        sys.exit(0)
