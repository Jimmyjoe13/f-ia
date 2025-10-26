# Documentation du Langage F-IA

## Table des Matières
1. [Introduction](#introduction)
2. [Syntaxe de Base](#syntaxe-de-base)
3. [Types de Données](#types-de-données)
4. [Variables](#variables)
5. [Opérateurs](#opérateurs)
6. [Structures de Contrôle](#structures-de-contrôle)
7. [Fonctions](#fonctions)
8. [Listes](#listes)
9. [Fonctions Intégrées](#fonctions-intégrées)
10. [REPL](#repl)
11. [Exemples](#exemples)

---

## Introduction

F-IA est un langage de programmation expérimental conçu pour être accessible et expressif en français. Il vise à fournir une base solide pour l'apprentissage de la programmation et l'exploration de concepts liés à l'IA.

---

## Syntaxe de Base

- **Commentaires** : Les commentaires ne sont pas implémentés dans cette version.
- **Séparateurs** : Les instructions peuvent être séparées par des sauts de ligne ou des point-virgules (`;`).
- **Indentation** : L'indentation n'est pas significative pour le parsing, mais est recommandée pour la lisibilité.
- **Identifiants** : Les noms de variables et de fonctions doivent commencer par une lettre ou un underscore (`_`) et ne peuvent contenir que des lettres, chiffres, ou underscores. Les caractères accentués ne sont pas supportés dans les identifiants.
- **Mots-clés** : Les mots-clés sont réservés et doivent être en minuscules.

---

## Types de Données

- **Entier (Integer)** : `123`, `-456`
- **Décimal (Float)** : `3.14`, `-2.5`
- **Chaîne de Caractères (String)** : `"Bonjour"`, `'Monde'`
- **Booléen (Boolean)** : `vrai`, `faux`
- **Liste (List)** : `[1, "deux", 3.0]`
- **Nul (Null)** : `nul` (non implémenté dans cette version)

---

## Variables

### Déclaration et Assignation

- **Déclaration avec initialisation** : Utilisez `soit` pour déclarer une nouvelle variable et lui attribuer une valeur.
  ```f-ia
  soit nom_variable = valeur
  ```
  Exemple :
  ```f-ia
  soit age = 25
  soit nom = "Alice"
  soit est_actif = vrai
  ```

- **Réassignation** : Vous pouvez réassigner une nouvelle valeur à une variable existante en utilisant l'opérateur `=`.
  ```f-ia
  nom_variable = nouvelle_valeur
  ```
  Exemple :
  ```f-ia
  age = age + 1
  ```

---

## Opérateurs

### Opérateurs Arithmétiques

- `+` (Addition)
- `-` (Soustraction)
- `*` (Multiplication)
- `/` (Division)
- `%` (Modulo)
- `-` (Négation unaire - non implémenté dans cette version)

### Opérateurs de Comparaison

- `==` (Égal à)
- `!=` (Différent de)
- `<` (Inférieur à)
- `>` (Supérieur à)
- `<=` (Inférieur ou égal à)
- `>=` (Supérieur ou égal à)

### Opérateurs Logiques

- `et` (ET logique)
- `ou` (OU logique)

### Priorité des Opérateurs

De la plus haute à la plus basse :
1. `()` (Parenthèses)
2. `*`, `/`, `%` (Multiplication, Division, Modulo)
3. `+`, `-` (Addition, Soustraction)
4. `<`, `>`, `<=`, `>=` (Comparaison)
5. `==`, `!=` (Égalité)
6. `et` (ET logique)
7. `ou` (OU logique)
8. `=` (Assignation)

---

## Structures de Contrôle

### Condition `si` / `sinon`

Exécute un bloc de code si une condition est vraie. Un bloc `sinon` optionnel s'exécute si la condition est fausse.

```f-ia
si (condition) {
    // instructions si la condition est vraie
} sinon {
    // instructions si la condition est fausse (optionnel)
}
```

Exemple :
```f-ia
soit note = 15
si (note >= 10) {
    imprimer("Admis")
} sinon {
    imprimer("Recalé")
}
```

### Boucle `tant_que`

Répète un bloc de code tant qu'une condition est vraie. Une sécurité limite les boucles à 50 itérations pour éviter les boucles infinies accidentelles.

```f-ia
tant_que (condition) {
    // instructions à répéter
}
```

Exemple :
```f-ia
soit i = 0
tant_que (i < 3) {
    imprimer(i)
    i = i + 1
}
```

### Boucle `pour`

Répète un bloc de code pour une série de valeurs, généralement en incrémentant ou décrémentant un compteur.

```f-ia
pour (initialisation; condition; increment) {
    // instructions à répéter
}
```

Exemple :
```f-ia
pour (soit j = 0; j < 3; j = j + 1) {
    imprimer(j)
}
```

---

## Fonctions

### Définition

Définit une fonction nommée avec des paramètres optionnels.

```f-ia
fonction nom_fonction(param1, param2, ...) {
    // corps de la fonction
    // utilisez 'retourner' pour renvoyer une valeur
}
```

Exemple :
```f-ia
fonction saluer(nom) {
    imprimer("Bonjour, " + nom + "!")
}
```

### Appel de Fonction

Appelle une fonction définie précédemment avec des arguments.

```f-ia
nom_fonction(argument1, argument2, ...)
```

Exemple :
```f-ia
saluer("Bob")
```

### Valeur de Retour

Utilisez le mot-clé `retourner` dans le corps d'une fonction pour renvoyer une valeur et sortir immédiatement de la fonction. Si `retourner` n'est pas utilisé, la fonction retourne `nul`.

```f-ia
fonction doubler(nombre) {
    retourner nombre * 2
}
soit resultat = doubler(5)
imprimer(resultat) // Affiche 10
```

### Portée des Variables

Les variables déclarées à l'intérieur d'une fonction sont **locales** à cette fonction. Elles ne sont pas accessibles en dehors de celle-ci.

---

## Listes

Les listes sont des collections ordonnées de valeurs.

### Création

```f-ia
soit ma_liste = [element1, element2, ...]
```

Exemple :
```f-ia
soit nombres = [1, 2, 3, 4]
soit melange = [1, "deux", vrai, 3.14]
```

### Accès aux Éléments

L'accès aux éléments par index (ex: `liste[0]`) n'est pas implémenté dans cette version.

---

## Fonctions Intégrées

Le langage fournit un ensemble de fonctions intégrées.

- `imprimer(...)` : Affiche les arguments sur la sortie standard.
- `longueur(objet)` : Retourne la longueur d'une chaîne ou d'une liste.
- `arrondir(nombre, decimales)` : Arrondit un nombre. `decimales` est optionnel.
- `aleatoire()` : Génère un nombre aléatoire entre 0 et 1.
- `racine(nombre)` : Calcule la racine carrée d'un nombre.
- `puissance(base, exposant)` : Calcule `base` élevé à la puissance `exposant`.
- `entier(valeur)` : Convertit une valeur en entier.
- `chaine(valeur)` : Convertit une valeur en chaîne de caractères.

---

## REPL

F-IA inclut un environnement de lecture-évaluation-impression (REPL) interactif.

### Commandes Spéciales

- `f-ia> ...` : Invite de commande pour taper des instructions.
- `.aide` : Affiche un court message d'aide.
- `.variables` : Affiche la liste des variables globales actuellement définies.
- `.reset` : Réinitialise toutes les variables et fonctions définies par l'utilisateur.
- `.quitter` ou `quitter` : Quitte le REPL.

---

## Exemples

### Exemple 1 : Calcul Simple

```f-ia
soit a = 10
soit b = 20
soit somme = a + b
imprimer("La somme est ", somme)
```

### Exemple 2 : Boucle et Condition

```f-ia
soit liste = [1, 2, 3, 4, 5]
soit i = 0
tant_que (i < longueur(liste)) {
    si (liste[i] % 2 == 0) {
        imprimer(liste[i], " est pair")
    } sinon {
        imprimer(liste[i], " est impair")
    }
    i = i + 1
}
```

### Exemple 3 : Fonction Personnalisée avec `retourner`

```f-ia
fonction factoriel(n) {
    si (n <= 1) {
        retourner 1
    } sinon {
        retourner n * factoriel(n - 1)
    }
}
soit resultat = factoriel(5)
imprimer("5! = ", resultat)
```
>>>>>>> 44e498ba6f849a2760e48468ba6ed85c985ef605
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
git clone https://github.com/Jimmyjoe13/f-ia-2.git
cd f-ia-2
pip install -r requirements.txt
```

## ⚙️ Configuration IA (actuelle)

Créez un fichier `.env` à la racine du projet :
```env
# OpenAI
OPENAI_API_KEY=votre_cle_openai_ici
DEFAULT_OPENAI_MODEL=gpt-4.1-nano

# DeepSeek
DEEPSEEK_API_KEY=votre_cle_deepseek_ici
DEFAULT_DEEPSEEK_MODEL=deepseek-chat
```

> Note: le support Anthropic (Claude) n'est pas encore intégré. Il sera ajouté après le système de modules/imports.

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

## 🔥 Intégration IA Générative (actuelle)

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

## 🏗️ Architecture technique

- **Lexer** (`lexer.py`) - Analyse lexicale (inclut commentaires `#` et `//`)
- **Parser** (`parser.py`) - Analyse syntaxique (assignations composées, pour...dans)
- **AST** (`fia_ast.py`) - Nœuds de syntaxe (AssignationComposee, BouclePourDans, ...)
- **Interpréteur** (`interpreter.py`) - Exécution (listes, dictionnaires, IA, pour...dans)
- **Fonctions intégrées** (`builtin.py`) - Bibliothèque standard (conversions robustes)
- **Intégration IA** (`ai_integration.py`) - OpenAI, DeepSeek
- **Module IA** (`ia_module.py`) - Fonctions d'intelligence artificielle
- **REPL** (`repl.py`) - Interface interactive
- **Gestion d'erreurs** (`errors.py`) - Système d'erreurs enrichi

## 📦 Requirements

- Python 3.10+
- `openai`
- Variables d'environnement `.env` comme indiqué plus haut

## 🗺️ Roadmap (prochaines étapes)

- **Système de modules / imports (PRIORITÉ)**
  - Syntaxe cible initiale: `importer "utils.fia"`
  - Résolution relative au fichier courant + chemins de recherche (`./`, `./lib`, `FIA_PATH`)
  - Cache des modules (chargement unique)
  - Contexte isolé par module et injection des symboles
  - Exemples et tests: `exemples/modules/`
- **Support Anthropic (Claude)** (après modules/imports)
- **Génération d'images** (DALL-E / Stable Diffusion)
- **Améliorations REPL** (historique, multi-lignes, chargement de modules)

---

**F-IA v1.2 (en cours)** - pour...dans, conversions robustes, et modules/imports à venir 🚀
=======
# Documentation du Langage F-IA

## Table des Matières
1. [Introduction](#introduction)
2. [Syntaxe de Base](#syntaxe-de-base)
3. [Types de Données](#types-de-données)
4. [Variables](#variables)
5. [Opérateurs](#opérateurs)
6. [Structures de Contrôle](#structures-de-contrôle)
7. [Fonctions](#fonctions)
8. [Listes](#listes)
9. [Fonctions Intégrées](#fonctions-intégrées)
10. [REPL](#repl)
11. [Exemples](#exemples)

---

## Introduction

F-IA est un langage de programmation expérimental conçu pour être accessible et expressif en français. Il vise à fournir une base solide pour l'apprentissage de la programmation et l'exploration de concepts liés à l'IA.

---

## Syntaxe de Base

- **Commentaires** : Les commentaires ne sont pas implémentés dans cette version.
- **Séparateurs** : Les instructions peuvent être séparées par des sauts de ligne ou des point-virgules (`;`).
- **Indentation** : L'indentation n'est pas significative pour le parsing, mais est recommandée pour la lisibilité.
- **Identifiants** : Les noms de variables et de fonctions doivent commencer par une lettre ou un underscore (`_`) et ne peuvent contenir que des lettres, chiffres, ou underscores. Les caractères accentués ne sont pas supportés dans les identifiants.
- **Mots-clés** : Les mots-clés sont réservés et doivent être en minuscules.

---

## Types de Données

- **Entier (Integer)** : `123`, `-456`
- **Décimal (Float)** : `3.14`, `-2.5`
- **Chaîne de Caractères (String)** : `"Bonjour"`, `'Monde'`
- **Booléen (Boolean)** : `vrai`, `faux`
- **Liste (List)** : `[1, "deux", 3.0]`
- **Nul (Null)** : `nul` (non implémenté dans cette version)

---

## Variables

### Déclaration et Assignation

- **Déclaration avec initialisation** : Utilisez `soit` pour déclarer une nouvelle variable et lui attribuer une valeur.
  ```f-ia
  soit nom_variable = valeur
  ```
  Exemple :
  ```f-ia
  soit age = 25
  soit nom = "Alice"
  soit est_actif = vrai
  ```

- **Réassignation** : Vous pouvez réassigner une nouvelle valeur à une variable existante en utilisant l'opérateur `=`.
  ```f-ia
  nom_variable = nouvelle_valeur
  ```
  Exemple :
  ```f-ia
  age = age + 1
  ```

---

## Opérateurs

### Opérateurs Arithmétiques

- `+` (Addition)
- `-` (Soustraction)
- `*` (Multiplication)
- `/` (Division)
- `%` (Modulo)
- `-` (Négation unaire - non implémenté dans cette version)

### Opérateurs de Comparaison

- `==` (Égal à)
- `!=` (Différent de)
- `<` (Inférieur à)
- `>` (Supérieur à)
- `<=` (Inférieur ou égal à)
- `>=` (Supérieur ou égal à)

### Opérateurs Logiques

- `et` (ET logique)
- `ou` (OU logique)

### Priorité des Opérateurs

De la plus haute à la plus basse :
1. `()` (Parenthèses)
2. `*`, `/`, `%` (Multiplication, Division, Modulo)
3. `+`, `-` (Addition, Soustraction)
4. `<`, `>`, `<=`, `>=` (Comparaison)
5. `==`, `!=` (Égalité)
6. `et` (ET logique)
7. `ou` (OU logique)
8. `=` (Assignation)

---

## Structures de Contrôle

### Condition `si` / `sinon`

Exécute un bloc de code si une condition est vraie. Un bloc `sinon` optionnel s'exécute si la condition est fausse.

```f-ia
si (condition) {
    // instructions si la condition est vraie
} sinon {
    // instructions si la condition est fausse (optionnel)
}
```

Exemple :
```f-ia
soit note = 15
si (note >= 10) {
    imprimer("Admis")
} sinon {
    imprimer("Recalé")
}
```

### Boucle `tant_que`

Répète un bloc de code tant qu'une condition est vraie. Une sécurité limite les boucles à 50 itérations pour éviter les boucles infinies accidentelles.

```f-ia
tant_que (condition) {
    // instructions à répéter
}
```

Exemple :
```f-ia
soit i = 0
tant_que (i < 3) {
    imprimer(i)
    i = i + 1
}
```

### Boucle `pour`

Répète un bloc de code pour une série de valeurs, généralement en incrémentant ou décrémentant un compteur.

```f-ia
pour (initialisation; condition; increment) {
    // instructions à répéter
}
```

Exemple :
```f-ia
pour (soit j = 0; j < 3; j = j + 1) {
    imprimer(j)
}
```

---

## Fonctions

### Définition

Définit une fonction nommée avec des paramètres optionnels.

```f-ia
fonction nom_fonction(param1, param2, ...) {
    // corps de la fonction
    // utilisez 'retourner' pour renvoyer une valeur
}
```

Exemple :
```f-ia
fonction saluer(nom) {
    imprimer("Bonjour, " + nom + "!")
}
```

### Appel de Fonction

Appelle une fonction définie précédemment avec des arguments.

```f-ia
nom_fonction(argument1, argument2, ...)
```

Exemple :
```f-ia
saluer("Bob")
```

### Valeur de Retour

Utilisez le mot-clé `retourner` dans le corps d'une fonction pour renvoyer une valeur et sortir immédiatement de la fonction. Si `retourner` n'est pas utilisé, la fonction retourne `nul`.

```f-ia
fonction doubler(nombre) {
    retourner nombre * 2
}
soit resultat = doubler(5)
imprimer(resultat) // Affiche 10
```

### Portée des Variables

Les variables déclarées à l'intérieur d'une fonction sont **locales** à cette fonction. Elles ne sont pas accessibles en dehors de celle-ci.

---

## Listes

Les listes sont des collections ordonnées de valeurs.

### Création

```f-ia
soit ma_liste = [element1, element2, ...]
```

Exemple :
```f-ia
soit nombres = [1, 2, 3, 4]
soit melange = [1, "deux", vrai, 3.14]
```

### Accès aux Éléments

L'accès aux éléments par index (ex: `liste[0]`) n'est pas implémenté dans cette version.

---

## Fonctions Intégrées

Le langage fournit un ensemble de fonctions intégrées.

- `imprimer(...)` : Affiche les arguments sur la sortie standard.
- `longueur(objet)` : Retourne la longueur d'une chaîne ou d'une liste.
- `arrondir(nombre, decimales)` : Arrondit un nombre. `decimales` est optionnel.
- `aleatoire()` : Génère un nombre aléatoire entre 0 et 1.
- `racine(nombre)` : Calcule la racine carrée d'un nombre.
- `puissance(base, exposant)` : Calcule `base` élevé à la puissance `exposant`.
- `entier(valeur)` : Convertit une valeur en entier.
- `chaine(valeur)` : Convertit une valeur en chaîne de caractères.

---

## REPL

F-IA inclut un environnement de lecture-évaluation-impression (REPL) interactif.

### Commandes Spéciales

- `f-ia> ...` : Invite de commande pour taper des instructions.
- `.aide` : Affiche un court message d'aide.
- `.variables` : Affiche la liste des variables globales actuellement définies.
- `.reset` : Réinitialise toutes les variables et fonctions définies par l'utilisateur.
- `.quitter` ou `quitter` : Quitte le REPL.

---

## Exemples

### Exemple 1 : Calcul Simple

```f-ia
soit a = 10
soit b = 20
soit somme = a + b
imprimer("La somme est ", somme)
```

### Exemple 2 : Boucle et Condition

```f-ia
soit liste = [1, 2, 3, 4, 5]
soit i = 0
tant_que (i < longueur(liste)) {
    si (liste[i] % 2 == 0) {
        imprimer(liste[i], " est pair")
    } sinon {
        imprimer(liste[i], " est impair")
    }
    i = i + 1
}
```

### Exemple 3 : Fonction Personnalisée avec `retourner`

```f-ia
fonction factoriel(n) {
    si (n <= 1) {
        retourner 1
    } sinon {
        retourner n * factoriel(n - 1)
    }
}
soit resultat = factoriel(5)
imprimer("5! = ", resultat)
```
>>>>>>> 44e498ba6f849a2760e48468ba6ed85c985ef605
