# F-IA - Langage de Programmation Français pour l'Intelligence Artificielle 🤖

**F-IA** est un langage de programmation en français spécialement conçu pour l'apprentissage et le développement d'applications d'intelligence artificielle.

## 🌟 Caractéristiques

- **Syntaxe française** intuitive et accessible
- **Support des caractères accentués** (é, è, à, ç, etc.)
- **Dictionnaires natifs** avec accès par clé
- **Pipeline IA complet** intégré
- **REPL interactif** avec debug détaillé
- **Gestion d'erreurs avancée** avec localisation ligne/colonne
- **30+ fonctions intégrées** pour manipulation de données
- **🔥 IA générative intégrée** - OpenAI, DeepSeek, Anthropic (Claude)
- **🆕 Chatbot conversationnel** - Exemples complets inclus
- **🆕 Support "sinon si"** - Syntaxe conditionnelle enrichie
- **🆕 Interaction utilisateur** - Fonctions `lire()` et `arreter()`
- **🆕 Commentaires** - `# ...` et `// ...` (ligne)
- **🆕 Opérateurs d'assignation** - `+=`, `-=`, `*=`, `/=`, `%=`
- **🆕 Boucle `pour...dans`** - Itération sur listes, dictionnaires et chaînes
- **🆕 Conversions robustes** - `entier()`, `decimal()`, `chaine()`, `booleen()`

## 📦 Installation

```bash
git clone https://github.com/Jimmyjoe13/f-ia-2.git
cd f-ia-2
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

# Anthropic (Claude)
ANTHROPIC_API_KEY=votre_cle_anthropic_ici
DEFAULT_ANTHROPIC_MODEL=claude-3-5-sonnet-latest
```

> Assurez-vous d'installer aussi la dépendance `anthropic` si vous utilisez Claude (voir Requirements).

## 🚀 Utilisation

### Mode interactif (REPL)
```bash
python main.py
```

### Exécution de fichiers
```bash
python main.py mon_script.fia
```

### 🤖 Démo Chatbot Simple
```bash
python main.py exemples/chatbot_simple.fia
```

### 🔥 Démo Chatbot IA Avancé
```bash
python main.py exemples/chatbot_ia_avance.fia
```

### 🧪 Tests récents
```bash
python main.py exemples/test_pour_dans.fia     # boucle pour...dans + assignations composées
python main.py exemples/test_conversions.fia   # conversions robustes
```

## ✨ Nouveautés récentes

- **Boucle `pour...dans`** sur listes, dictionnaires (clés) et chaînes
- **Conversions robustes**: `entier()`, `decimal()`, `chaine()`, `booleen()`
- **Amélioration accès dictionnaires**: support de `dict[cle]` même quand la clé est une variable
- **Opérateurs d'assignation composés**: `+=`, `-=`, `*=`, `/=`, `%=`
- **Commentaires ligne**: `#` et `//` ignorés jusqu'à fin de ligne

Extrait `exemples/test_pour_dans.fia`:
```fia
soit noms = ["Alice", "Bob", "Charlie"]
imprimer("🔹 Itération sur une liste:")
pour nom dans noms {
    imprimer("  Bonjour", nom)
}

soit ages = {"Alice": 25, "Bob": 30, "Charlie": 35}
imprimer("\n🔹 Itération sur un dictionnaire (clés):")
pour personne dans ages {
    imprimer("  ", personne, "a", ages[personne], "ans")
}

soit mot = "F-IA"
imprimer("\n🔹 Itération sur une chaîne:")
pour lettre dans mot {
    imprimer("  Lettre:", lettre)
}
```

Extrait `exemples/test_conversions.fia`:
```fia
imprimer("== Tests entier() ==")
imprimer(entier("12"))
imprimer(entier("  -3 "))
imprimer(entier("12.9"))
imprimer(entier(3.7))
imprimer(entier(vrai))
imprimer(entier(faux))
imprimer(entier(nul))

imprimer("\n== Tests decimal() ==")
imprimer(decimal("12"))
imprimer(decimal("  -3.25 "))
imprimer(decimal(5))
imprimer(decimal(faux))
imprimer(decimal(nul))

imprimer("\n== Tests chaine() ==")
imprimer(chaine(123))
imprimer(chaine(4.56))
imprimer(chaine(vrai))
imprimer(chaine(nul))
soit l = [1, 2, 3]
soit d = {"a": 1, "b": 2}
imprimer(chaine(l))
imprimer(chaine(d))

imprimer("\n== Tests booleen() ==")
imprimer(booleen(0), booleen(1), booleen(-1))
imprimer(booleen("true"), booleen("FALSE"), booleen("ok"))
imprimer(booleen(""), booleen(nul))
imprimer(booleen([]), booleen([0]))
imprimer(booleen({}), booleen({"x":1}))
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

### Dictionnaires
```fia
soit utilisateur = {"nom": "Alice", "age": 25, "ville": "Paris"}
imprimer(utilisateur["nom"])        # Alice
utilisateur["age"] = 26             # Modification
utilisateur["profession"] = "Dev"   # Ajout de clé
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

### Boucles (classique)
```fia
# Boucle tant que
soit i = 0
tant_que (i < 5) {
    imprimer("Compteur:", i)
    i = i + 1
}

# Boucle pour (style C)
pour (soit j = 0; j < longueur(notes); j = j + 1) {
    imprimer("Note:", notes[j])
}
```

### Boucle `pour...dans`
```fia
pour nom dans ["Alice", "Bob"] {
  imprimer("Bonjour", nom)
}
```

## 🔥 Intégration IA Générative

### Appel direct aux IA
```fia
soit reponse = appeler_ia("openai", "gpt-4.1-nano", "Explique-moi la programmation")
imprimer("OpenAI:", reponse)

soit code = appeler_ia("deepseek", "deepseek-coder", "Écris une fonction de tri en Python")
imprimer("DeepSeek:", code)

soit claude = appeler_ia("anthropic", nul, "Dis bonjour en 1 phrase")
imprimer("Claude:", claude)
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

## 🏗️ Architecture technique

- **Lexer** (`lexer.py`) - Analyse lexicale (inclut commentaires `#` et `//`)
- **Parser** (`parser.py`) - Analyse syntaxique (assignations composées, pour...dans)
- **AST** (`fia_ast.py`) - Nœuds de syntaxe (AssignationComposee, BouclePourDans, ...)
- **Interpréteur** (`interpreter.py`) - Exécution (listes, dictionnaires, IA, pour...dans)
- **Fonctions intégrées** (`builtin.py`) - Bibliothèque standard (conversions robustes)
- **Intégration IA** (`ai_integration.py`) - OpenAI, DeepSeek, Anthropic
- **Module IA** (`ia_module.py`) - Fonctions d'intelligence artificielle
- **REPL** (`repl.py`) - Interface interactive
- **Gestion d'erreurs** (`errors.py`) - Système d'erreurs enrichi

## 📦 Requirements

- Python 3.10+
- `openai`
- `anthropic` (si vous activez Claude)
- Variables d'environnement `.env` comme indiqué plus haut

## 🗺️ Roadmap (prochaines étapes)

- **Système de modules / imports**
  - Syntaxe cible: `importer "utils.fia"` ou `importer utilitaires de "./lib/utils.fia"`
  - Portées: variables du module isolées; export explicite ou import sélectif
  - Cache de modules et résolution relative au fichier courant
  - Chemins de recherche (ex: `./`, `./lib`, `FIA_PATH`)
  - Exemples et tests: `exemples/modules/`
- **Génération d'images** (DALL-E / Stable Diffusion)
- **Améliorations REPL** (historique, multi-lignes, chargement de modules)

---

**F-IA v1.2** - pour...dans, conversions robustes, et Claude (Anthropic) 🚀
