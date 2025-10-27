# F-IA - Langage de Programmation Français avec IA Native 🤖

**F-IA** est un langage de programmation en français spécialement conçu pour l'apprentissage et le développement d'applications d'intelligence artificielle.

## 🎉 VERSION 2.0 LIVRÉE : ML Natif avec scikit-learn

F-IA dispose désormais d'un **backend Machine Learning natif** (scikit-learn, pandas, numpy) exposé via un module F-IA simple, permettant classification, régression, clustering, preprocessing et validation croisée.

- Nouveau module: `lib/ml.fia`
- Nouveau backend Python: `ml_backend.py`
- Nouveaux exemples: `exemples/test_ml_basic.fia`, `exemples/test_csv_ml.fia`, `exemples/demo_ml_complet.fia`

## 📦 Écosystème de modules (v1.5)

F-IA inclut un **écosystème de 7 modules intégrés** avec **+60 fonctions**.

### Syntaxe des modules
```fia
importer "lib/texte.fia" comme texte
importer "lib/fichiers.fia" comme fichiers
importer "lib/utils.fia" comme utils
importer "lib/web.fia" comme web

soit slug = texte.generer_slug("Mon Article Français !")
soit infos = fichiers.info_fichier("/home/user/document.pdf")
soit date = utils.formater_date(2025, 10, 27)
soit api_url = web.construire_url("https", "api.exemple.com", "/v1/articles")

depuis "lib/math.fia" importer PI, carre, racine_carree
imprimer("Aire du cercle:", PI * carre(5))
```

### Fonctionnalités modules
- ✅ Import avec alias: `importer "module.fia" comme nom`
- ✅ Import sélectif: `depuis "module.fia" importer f1, f2`
- ✅ Accès attributs: `module.fonction()`, `module.variable`
- ✅ Cache intelligent et détection de cycles
- ✅ Chemins de recherche: `./`, `./lib/`, `FIA_PATH`
- ✅ Espaces de noms isolés

## 🌟 Caractéristiques du langage

- Syntaxe française lisible et expressive
- Dictionnaires natifs, boucles `pour...dans`, `sinon si`, opérateurs `+= -= *= /= %=`
- Conversions robustes: `entier()`, `decimal()`, `chaine()`, `booleen()`
- REPL interactif, erreurs localisées, 60+ fonctions intégrées
- IA générative (OpenAI, DeepSeek): chatbot et appels LLM

## 📦 Installation
```bash
git clone https://github.com/Jimmyjoe13/f-ia.git
cd f-ia
pip install -r requirements.txt
```

## ⚙️ Configuration IA
Créez `.env` à la racine:
```env
OPENAI_API_KEY=...
DEFAULT_OPENAI_MODEL=gpt-4.1-nano
DEEPSEEK_API_KEY=...
DEFAULT_DEEPSEEK_MODEL=deepseek-chat
```

## 🚀 Utilisation

Mode interactif (REPL)
```bash
python main.py
```

Exécuter un fichier
```bash
python main.py mon_script.fia
```

Aide et exemples utiles
```bash
python main.py exemples/test_texte.fia
python main.py exemples/test_fichiers.fia
python main.py exemples/test_utils.fia
python main.py exemples/test_web.fia
python main.py exemples/app_demo_complete.fia
python main.py exemples/showcase_final.fia
python main.py exemples/test_api_reelle.fia
python main.py exemples/test_modules.fia
python main.py exemples/demo_complete.fia
python main.py exemples/chatbot_ia_avance.fia
# Nouveaux exemples ML (v2.0)
python main.py exemples/test_ml_basic.fia
python main.py exemples/test_csv_ml.fia
python main.py exemples/demo_ml_complet.fia
```

## 🔥 Intégration ML Natif (v2.0)

- Module F-IA: `lib/ml.fia` expose:
  - Données: `charger_csv`, `separer_features_target` (retourne {"X": ..., "y": ...})
  - Preprocessing: `standardiser_donnees`, `normaliser_donnees`
  - Classifieurs: `RandomForestClassifier(n_arbres, profondeur_max)`, `SVM(kernel, C)`, `KNNClassifier(k)`
  - Régressions: `LinearRegression()`, `RandomForestRegressor(n_arbres, profondeur_max)`
  - Clustering: `KMeans(k, max_iter)`, `clustering_hierarchique(n_clusters)`
  - Entraînement/évaluation: `entrainer`, `predire`, `evaluer_modele`, `validation_croisee`, `matrice_confusion`, `rapport_classification`
- Backend Python: `ml_backend.py` implémente scikit-learn/pandas/numpy avec gestion d'erreurs explicites

Exemple rapide
```fia
importer "lib/ml.fia" comme ml
soit data = ml.charger_csv("exemples/iris_simple.csv")
soit split = ml.separer_features_target(data, "species")
soit X = split["X"]
soit y = split["y"]
soit Xs = ml.standardiser_donnees(X)
soit m = ml.RandomForestClassifier(100, nul)
ml.entrainer(m, Xs, y)
soit acc = ml.evaluer_modele(m, Xs, y, "accuracy")
imprimer("Accuracy:", acc)
```

## 🌐 Exemple Complet: Application Web d'Analyse SEO (NOUVEAU)

Cette application montre comment créer une **application SEO réelle** en F-IA :
- Extraction HTML réelle via `requests` (backend `ml_backend.py`)
- Analyse: titre, meta description, structure H1/H2/H3, contenu, liens, images, technique
- Score global sur 100 avec recommandations
- Rapport HTML généré (aperçu en console)

### Arborescence
```
exemples/seo_analyzer/
├── seo_scraper.fia      # Extraction (réelle) du HTML + parsing simple
├── seo_analyzer.fia     # Calcul des scores/diagnostics SEO
├── seo_reporter.fia     # Génération d'un rapport HTML (console)
└── seo_main.fia         # Interface utilisateur interactive (menu)
```

### Pré-requis
- Assurez-vous d'avoir `requests` installé (déjà dans `requirements.txt`)
- Le fichier `ml_backend.py` inclut une fonction `faire_requete_web(url)` exposée à F-IA via `appeler_python_ml`

### Lancer l'application SEO (interface)
```bash
python main.py exemples/seo_analyzer/seo_main.fia
```

### Exemple rapide (test unitaire)
```bash
python main.py exemples/seo_analyzer/test_scraper.fia
python main.py exemples/seo_analyzer/test_analyzer.fia
python main.py exemples/seo_analyzer/test_complet.fia
```

### Ce que vous verrez
- Status HTTP, taille HTML réelle
- Titre/meta détectés, nombre de H1/H2/H3, liens, images
- Score global et sections détaillées
- Aperçu d'un rapport HTML généré (chemin: `rapports/rapport_seo_*.html` simulé)

## 📚 Autres modules clés
- `lib/texte.fia`, `lib/fichiers.fia`, `lib/utils.fia`, `lib/web.fia`, `lib/math.fia`, `lib/collections.fia`

## 🏗️ Architecture technique
- Lexer/Parser/AST: `lexer.py`, `parser.py`, `fia_ast.py`
- Interpréteur: `interpreter.py` (espaces de noms, modules, appels)
- Résolution de modules: `module_resolver.py`
- Builtins: `builtin.py` (IA générative + ponts ML)
- Backends: `ai_integration.py`, `ia_module.py`, `ml_backend.py`
- REPL: `repl.py` / `fia_repl.py`

## 🗺️ Roadmap

### ✅ Phase 1 – Système de modules
- Imports, espaces de noms, cache, détection de cycles, modules de base

### ✅ Phase 1.5 – Écosystème de modules
- 7 modules, +60 fonctions, apps de démonstration, tests auto

### ✅ Phase 3.1 – Machine Learning Natif (LIVRÉ)
- scikit-learn, pandas, numpy intégrés
- Classification, régression, clustering, preprocessing
- Validation croisée, métriques, exemples fonctionnels

### 🚧 Phase 3.2 – Deep Learning
- TensorFlow (Keras) et PyTorch: denses, CNN, RNN, LSTM, Attention
- Accélération GPU (CUDA) quand disponible

### 🚧 Phase 3.3 – Vision & Données
- OpenCV (vision), pandas avancé, chargeurs CSV/JSON/Excel/DB, visualisation (matplotlib/seaborn)

### 🛠️ Phase 4 – Tooling pro
- Extension VS Code, formateur, linter, package manager, debugger, bytecode

## 💡 Applications réalisables
- Chatbots, analyseurs de données, clients API, gestionnaires de fichiers, générateurs de contenu, tableaux de bord, apps industrielles
- ML: classification, régression, clustering, validation
- 🌐 SEO: Analyseur SEO web complet (exemple ci-dessus)

## 📞 Support et Contribution
- Repository: https://github.com/Jimmyjoe13/f-ia
- Issues & PR bienvenues

---

**F-IA v2.0** – Premier langage de programmation français avec ML natif prêt pour l'industrie 🚀🇫🇷
