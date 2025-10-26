# F-IA - Langage de Programmation Français avec IA Native 🤖

**F-IA** est un langage de programmation en français spécialement conçu pour l'apprentissage et le développement d'applications d'intelligence artificielle.

## 🎉 **NOUVEAUTÉ MAJEURE v1.5 : ÉCOSYSTÈME DE MODULES COMPLET !**

F-IA dispose maintenant d'un **écosystème de modules complet** avec **6 modules intégrés** qui permettent la création d'applications réelles multi-fichiers !

### 📦 **Syntaxe des modules**

```fia
# Import avec alias
importer "lib/texte.fia" comme texte
importer "lib/fichiers.fia" comme fichiers
importer "lib/utils.fia" comme utils

# Utilisation des modules
soit slug = texte.generer_slug("Mon Article Français !")
soit infos = fichiers.info_fichier("/home/user/document.pdf")
soit date = utils.formater_date(2025, 10, 26)

# Import sélectif
depuis "lib/math.fia" importer PI, carre, racine_carree
imprimer("Aire du cercle:", PI * carre(5))
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
- **🆕 Écosystème de modules** complet avec 6 modules intégrés
- **Support des caractères accentués** (é, è, à, ç, etc.)
- **Dictionnaires natifs** avec accès par clé
- **Pipeline IA complet** intégré
- **REPL interactif** avec debug détaillé
- **Gestion d'erreurs avancée** avec localisation ligne/colonne
- **50+ fonctions intégrées** pour manipulation de données
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

### 📦 Tests des modules
```bash
# Tester tous les modules
python main.py exemples/test_modules.fia
python main.py exemples/test_texte.fia
python main.py exemples/test_fichiers.fia
python main.py exemples/test_utils.fia

# Démonstration complète
python main.py exemples/demo_complete.fia
python main.py exemples/chatbot_ia_avance.fia
```

## 📚 **Modules intégrés**

### 📝 **`lib/texte.fia`** - Manipulation de chaînes **[NOUVEAU]**
```fia
importer "lib/texte.fia" comme texte

# Conversions de casse
imprimer(texte.majuscules("bonjour"))  # "BONJOUR"
imprimer(texte.titre("mon article"))   # "Mon Article"

# Nettoyage et validation
imprimer(texte.nettoyer_espaces("texte   avec   espaces"))
imprimer(texte.est_email("test@exemple.fr"))  # True
imprimer(texte.est_url("https://github.com"))  # True

# Génération de slugs
imprimer(texte.generer_slug("Mon Article Français!"))  # "mon-article-francais"

# Statistiques
soit stats = texte.statistiques_texte("Bonjour, comment allez-vous ?")
imprimer("Mots:", stats["mots"], "Longueur:", stats["longueur"])
```

### 📁 **`lib/fichiers.fia`** - Gestion de fichiers **[NOUVEAU]**
```fia
importer "lib/fichiers.fia" comme fichiers

# Extraction d'informations
soit infos = fichiers.info_fichier("/home/user/document.pdf")
imprimer("Nom:", infos["nom"])                    # "document.pdf"
imprimer("Extension:", infos["extension"])         # "pdf"
imprimer("Sans extension:", infos["nom_sans_ext"]) # "document"

# Gestion des chemins
soit chemin = fichiers.joindre_chemins("/home/user", "documents/fichier.txt")
imprimer("Chemin joint:", chemin)  # "/home/user/documents/fichier.txt"

soit normalise = fichiers.normaliser_chemin("C:\\Users\\Jimmy\\file.txt")
imprimer("Normalisé:", normalise)  # "C:/Users/Jimmy/file.txt"

# Validation et génération
imprimer("Nom valide:", fichiers.valider_nom_fichier("document.pdf"))  # True
soit unique = fichiers.creer_nom_fichier_unique("backup", "zip")
imprimer("Nom unique:", unique)  # "backup_20251026_161200.zip"
```

### 🛠️ **`lib/utils.fia`** - Utilitaires divers **[NOUVEAU]**
```fia
importer "lib/utils.fia" comme utils

# Dates et heures
imprimer("Date actuelle:", utils.date_actuelle())  # "2025-10-26"
imprimer("Heure actuelle:", utils.heure_actuelle())  # "16:45:00"
soit date_formatee = utils.formater_date(2025, 12, 25)  # "2025-12-25"

# Validation avancée
imprimer("Est entier:", utils.est_nombre_entier("123"))      # True
imprimer("Est décimal:", utils.est_nombre_decimal("12.34"))  # True
imprimer("Email valide:", utils.valider_email_simple("test@exemple.fr"))

# Formatage utile
imprimer("Taille:", utils.formater_taille_octets(1536))      # "1.5 Ko"
imprimer("Pourcentage:", utils.formater_pourcentage(25, 100)) # "25.0%"

# Conversions pratiques
imprimer("°F:", utils.convertir_celsius_fahrenheit(25))  # 77.0
imprimer("km:", utils.convertir_metres_kilometres(1500)) # 1.5

# Génération et manipulation
soit mdp = utils.generer_mot_de_passe_simple(8)
soit liste_unique = utils.dedoublon_liste(["a", "b", "a", "c"])
```

### 🔢 **`lib/math.fia`** - Fonctions mathématiques
```fia
importer "lib/math.fia" comme math

imprimer("PI =", math.PI)                           # 3.14159...
imprimer("Carré de 7 =", math.carre(7))            # 49
imprimer("Racine de 16 =", math.racine_carree(16))  # 4.0
imprimer("Factorielle de 5 =", math.factorielle(5)) # 120
imprimer("Max de 10 et 20 =", math.maximum(10, 20)) # 20
```

### 🗂️ **`lib/collections.fia`** - Structures de données
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
importer "lib/texte.fia" comme texte
soit slug = texte.generer_slug("Mon Titre")

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

### Application complète multi-modules
```fia
# app_blog.fia - Générateur d'articles de blog
importer "lib/texte.fia" comme texte
importer "lib/fichiers.fia" comme fichiers
importer "lib/utils.fia" comme utils

fonction generer_article(titre, contenu, auteur) {
    # Générer slug pour URL
    soit slug = texte.generer_slug(titre)
    
    # Créer métadonnées
    soit metadata = {
        "titre": titre,
        "slug": slug,
        "auteur": auteur,
        "date": utils.date_actuelle(),
        "mots": texte.compter_mots(contenu),
        "taille": utils.formater_taille_octets(longueur(contenu))
    }
    
    # Générer nom de fichier unique
    soit nom_fichier = fichiers.creer_nom_fichier_unique(slug, "md")
    
    # Créer contenu Markdown
    soit markdown = "# " + titre + "\n\n"
    markdown += "*Par " + auteur + " - " + metadata["date"] + "*\n\n"
    markdown += contenu
    
    retourner {
        "fichier": nom_fichier,
        "contenu": markdown,
        "metadata": metadata
    }
}

# Utilisation
soit article = generer_article(
    "Mon Premier Article en F-IA",
    "F-IA est un langage révolutionnaire...",
    "Développeur F-IA"
)

imprimer("Article créé:")
imprimer("- Fichier:", article["fichier"])
imprimer("- Mots:", article["metadata"]["mots"])
imprimer("- Taille:", article["metadata"]["taille"])
```

## 🗺️ Roadmap

### ✅ **Phase 1 TERMINÉE - Système de modules**
- ✅ Import avec alias et import sélectif
- ✅ Résolution de chemins et cache
- ✅ Espaces de noms isolés
- ✅ Détection des cycles
- ✅ Modules de base (math, collections)

### ✅ **Phase 1.5 TERMINÉE - Écosystème de modules**
- ✅ `lib/texte.fia` - Manipulation avancée de chaînes
- ✅ `lib/fichiers.fia` - Gestion de fichiers et chemins
- ✅ `lib/utils.fia` - Utilitaires divers et conversions
- ✅ 6 modules complets avec +50 fonctions

### 🔄 **Phase 2 EN COURS - Extensions avancées**
- 🔄 `lib/web.fia` - Requêtes HTTP et APIs
- 🔄 Amélioration des messages d'erreur
- 🔄 Tests automatisés du langage
- 🔄 Documentation interactive

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

Avec l'écosystème de modules complet, F-IA permet maintenant de créer :

- **🤖 Chatbots intelligents** avec IA générative
- **📊 Applications d'analyse de données** avec validation et formatage
- **🌐 Scripts d'automatisation web** avec gestion de fichiers
- **📁 Outils de traitement de fichiers** avec manipulation de texte
- **🔬 Projets éducatifs en IA** avec modules pédagogiques
- **📱 Prototypes d'applications** avec écosystème complet
- **✍️ Générateurs de contenu** avec IA et formatage
- **🔧 Utilitaires système** avec validation et conversions

## 📞 Support et Contribution

- **Repository**: [https://github.com/Jimmyjoe13/f-ia](https://github.com/Jimmyjoe13/f-ia)
- **Issues**: Signalez les bugs et demandes de fonctionnalités
- **Pull Requests**: Contributions bienvenues !

---

**F-IA v1.5** - Le premier langage de programmation français avec écosystème de modules complet et IA native ! 🚀🇫🇷