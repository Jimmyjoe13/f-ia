# F-IA - Langage de Programmation Français avec IA Native 🤖

**F-IA** est un langage de programmation en français spécialement conçu pour l'apprentissage et le développement d'applications d'intelligence artificielle.

## 🎉 **NOUVEAUTÉ MAJEURE v1.4 : SYSTÈME DE MODULES !**

F-IA dispose maintenant d'un **système de modules complet et robuste** qui permet la réutilisation de code et l'organisation en projets multi-fichiers !

### 📦 **Syntaxe des modules**

```fia
# Import avec alias
importer "lib/math.fia" comme math
imprimer("PI =", math.PI)
imprimer("Carré de 5 =", math.carre(5))

# Import sélectif
depuis "lib/collections.fia" importer creer_pile, empiler, depiler
soit pile = creer_pile()
empiler(pile, "élément")
```

### 🏗️ **Fonctionnalités du système de modules**
- ✅ **Import avec alias** : `importer "module.fia" comme nom`
- ✅ **Import sélectif** : `depuis "module.fia" importer fonction1, fonction2`
- ✅ **Accès aux attributs** : `module.fonction()`, `module.variable`
- ✅ **Cache intelligent** : Chargement unique des modules
- ✅ **Détection des cycles** : Prévention des dépendances circulaires
- ✅ **Chemins de recherche** : `./`, `./lib/`, `FIA_PATH`
- ✅ **Espaces de noms** : Isolation complète entre modules

## 🌟 Caractéristiques

- **Syntaxe française** intuitive et accessible
- **🆕 Système de modules** complet avec import/export
- **Support des caractères accentués** (é, è, à, ç, etc.)
- **Dictionnaires natifs** avec accès par clé
- **Pipeline IA complet** intégré
- **REPL interactif** avec debug détaillé
- **Gestion d'erreurs avancée** avec localisation ligne/colonne
- **35+ fonctions intégrées** pour manipulation de données
- **🔥 IA générative intégrée** - OpenAI, DeepSeek
- **🆕 Chatbot conversationnel** - Exemples complets inclus
- **🆕 Support "sinon si"** - Syntaxe conditionnelle enrichie
- **🆕 Interaction utilisateur** - Fonctions `lire()` et `arreter()`
- **🆕 Commentaires** - `# ...` et `// ...` (ligne)
- **🆕 Opérateurs d'assignation** - `+=`, `-=`, `*=`, `/=`, `%=`
- **🆕 Boucle `pour...dans`** - Itération sur listes, dictionnaires et chaînes
- **🆕 Conversions robustes** - `entier()`, `decimal()`, `chaine()`, `booleen()`

## 📦 Installation

```bash
git clone https://github.com/Jimmyjoe13/f-ia.git
cd f-ia
pip install -r requirements.txt
```

## ⚙️ Configuration IA

Créez un fichier `.env` à la racine du projet :

```env
# OpenAI
OPENAI_API_KEY=votre_cle_openai_ici
DEFAULT_OPENAI_MODEL=gpt-4.1-nano

# DeepSeek
DEEPSEEK_API_KEY=votre_cle_deepseek_ici
DEFAULT_DEEPSEEK_MODEL=deepseek-chat
```

## 🚀 Utilisation

### Mode interactif (REPL)
```bash
python main.py
```

### Exécution de fichiers
```bash
python main.py mon_script.fia
```

### 📦 Démo du système de modules
```bash
python main.py exemples/test_modules.fia
python main.py exemples/demo_complete.fia
```

## 📚 **Modules disponibles**

### `lib/math.fia` - Module mathématique
```fia
importer "lib/math.fia" comme math

imprimer("PI =", math.PI)                    # 3.14159...
imprimer("Carré de 7 =", math.carre(7))     # 49
imprimer("Racine de 16 =", math.racine_carree(16))  # 4.0
imprimer("Factorielle de 5 =", math.factorielle(5)) # 120
imprimer("Max de 10 et 20 =", math.maximum(10, 20)) # 20
```

### `lib/collections.fia` - Structures de données
```fia
depuis "lib/collections.fia" importer creer_pile, empiler, depiler

soit pile = creer_pile()
empiler(pile, "Premier")
empiler(pile, "Deuxième")
imprimer("Dépilé:", depiler(pile))  # "Deuxième"
```

## 🔥 Intégration IA Générative

### Appel direct aux IA
```fia
soit reponse = appeler_ia("openai", "gpt-4.1-nano", "Explique-moi la programmation")
imprimer("OpenAI:", reponse)

soit code = appeler_ia("deepseek", "deepseek-coder", "Écris une fonction de tri en Python")
imprimer("DeepSeek:", code)
```

### Générer une réponse de chatbot
```fia
soit reponse_bot = generer_reponse_bot(
    "openai",
    nul,
    "Bonjour comment ça va ?",
    "Tu es un assistant sympa et serviable"
)
imprimer("Bot:", reponse_bot)
```

### 🤖 Démo Chatbot IA Avancé
```bash
python main.py exemples/chatbot_ia_avance.fia
```

## 📖 Syntaxe de base

### Variables et types
```fia
soit nom = "Alice"
soit âge = 25
soit notes = [15, 18, 12, 20]
soit actif = vrai
soit config = {"ville": "Paris", "pays": "France"}
```

### Modules et imports
```fia
# Import complet avec alias
importer "lib/math.fia" comme math
soit resultat = math.carre(5)

# Import sélectif
depuis "lib/utils.fia" importer formater_date, valider_email
soit date = formater_date(2025, 10, 26)
```

### Dictionnaires
```fia
soit utilisateur = {"nom": "Alice", "age": 25, "ville": "Paris"}
imprimer(utilisateur["nom"])  # Alice
utilisateur["age"] = 26       # Modification
utilisateur["profession"] = "Dev"  # Ajout de clé
```

### Conditions avec "sinon si"
```fia
si (âge >= 18) {
    imprimer("Majeur")
} sinon si (âge >= 13) {
    imprimer("Adolescent") 
} sinon {
    imprimer("Enfant")
}
```

### Boucle pour...dans
```fia
pour nom dans ["Alice", "Bob"] {
    imprimer("Bonjour", nom)
}

soit ages = {"Alice": 25, "Bob": 30}
pour personne dans ages {
    imprimer(personne, "a", ages[personne], "ans")
}
```

### Opérateurs d'assignation composés
```fia
soit x = 10
x += 5    # x devient 15
x *= 2    # x devient 30
x /= 3    # x devient 10.0
```

### Conversions robustes
```fia
imprimer(entier("123"))      # 123
imprimer(decimal("12.5"))    # 12.5
imprimer(chaine(42))         # "42"
imprimer(booleen("vrai"))    # vrai
```

## 🏗️ Architecture technique

- **Module Resolver** (`module_resolver.py`) - Système de résolution des modules
- **Lexer** (`lexer.py`) - Analyse lexicale avec support imports
- **Parser** (`parser.py`) - Analyse syntaxique avec nœuds d'import
- **AST** (`fia_ast.py`) - Nœuds pour ImportModule, ImportDepuis, AccesAttribut
- **Interpréteur** (`interpreter.py`) - Exécution avec espaces de noms
- **Fonctions intégrées** (`builtin.py`) - Bibliothèque standard
- **Intégration IA** (`ai_integration.py`) - OpenAI, DeepSeek
- **Module IA** (`ia_module.py`) - Fonctions d'intelligence artificielle
- **REPL** (`repl.py`) - Interface interactive avec support modules

## 📦 Requirements

- Python 3.10+
- `openai`
- Variables d'environnement `.env` pour les clés API

## 🎯 Exemples d'utilisation

### Projet multi-modules
```fia
# main.fia
importer "lib/math.fia" comme math
importer "lib/utils.fia" comme utils

fonction calculer_statistiques(donnees) {
    soit moyenne = math.somme(donnees) / longueur(donnees)
    soit rapport = {
        "moyenne": math.arrondir(moyenne, 2),
        "total": math.somme(donnees),
        "date": utils.date_actuelle()
    }
    retourner rapport
}

soit resultats = calculer_statistiques([10, 15, 8, 20, 12])
utils.sauvegarder_json("rapport.json", resultats)
```

## 🗺️ Roadmap

### ✅ **Phase 1 TERMINÉE - Système de modules**
- ✅ Import avec alias et import sélectif
- ✅ Résolution de chemins et cache
- ✅ Espaces de noms isolés
- ✅ Détection des cycles
- ✅ Modules de base (math, collections)

### 🔄 **Phase 1.5 EN COURS - Écosystème de modules**
- 🔄 `lib/texte.fia` - Manipulation avancée de chaînes
- 🔄 `lib/fichiers.fia` - Lecture/écriture de fichiers
- 🔄 `lib/web.fia` - Requêtes HTTP simples
- 🔄 `lib/utils.fia` - Utilitaires divers

### 📋 **Phase 2 - Syntaxe cohérente**
- Standardisation des règles syntaxiques
- Messages d'erreur améliorés
- Tests automatisés du langage
- Documentation interactive

### 🤖 **Phase 3 - Vraie intégration IA**
- Remplacement des simulations par scikit-learn
- Support TensorFlow/PyTorch
- Pipelines ML réels
- Support numpy/pandas natif

### 🛠️ **Phase 4 - Tooling**
- Extension VS Code pour F-IA
- Formateur de code automatique
- Linter et détection d'erreurs
- Package manager intégré

## 💡 Applications réalisables

Avec le système de modules, F-IA permet maintenant de créer :

- **🤖 Chatbots intelligents** avec IA générative
- **📊 Applications d'analyse de données** 
- **🌐 Scripts d'automatisation web**
- **📁 Outils de traitement de fichiers**
- **🔬 Projets éducatifs en IA**
- **📱 Prototypes d'applications**

## 📞 Support et Contribution

- **Repository**: [https://github.com/Jimmyjoe13/f-ia-2](https://github.com/Jimmyjoe13/f-ia)
- **Issues**: Signalez les bugs et demandes de fonctionnalités
- **Pull Requests**: Contributions bienvenues !

---

**F-IA v1.4** - Le premier langage de programmation français avec système de modules et IA native ! 🚀🇫🇷
