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
    // la dernière expression évaluée est la valeur de retour implicite
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

Pour le moment, la valeur de retour d'une fonction est la dernière expression évaluée dans son corps. La commande `retourner` n'est pas encore implémentée.

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

### Exemple 3 : Fonction Personnalisée

```f-ia
fonction factoriel(n) {
    si (n <= 1) {
        1
    } sinon {
        n * factoriel(n - 1)
    }
}
soit resultat = factoriel(5)
imprimer("5! = ", resultat)
```
```
