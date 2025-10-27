# ml_backend.py - Backend Machine Learning natif pour F-IA Phase 3
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix, classification_report
import json
import os
from errors import RuntimeError

# ===== NOUVELLE SECTION : WEB SCRAPING =====
def faire_requete_web(url):
    """Fait une vraie requête HTTP et retourne le contenu HTML"""
    try:
        import requests
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        print(f"🌐 [WEB] Requête HTTP vers: {url}")
        response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        
        print(f"✅ [WEB] Requête réussie - Status: {response.status_code}")
        print(f"📏 [WEB] Taille HTML: {len(response.text)} caractères")
        
        return {
            "html": response.text,
            "status": response.status_code,
            "url": response.url,
            "headers": dict(response.headers),
            "encoding": response.encoding or 'utf-8'
        }
        
    except ImportError:
        return {
            "erreur": "Module 'requests' non installé. Exécutez: pip install requests"
        }
    except requests.exceptions.Timeout:
        return {
            "erreur": f"Timeout lors de l'accès à {url} (15 secondes dépassées)"
        }
    except requests.exceptions.ConnectionError:
        return {
            "erreur": f"Impossible de se connecter à {url}"
        }
    except requests.exceptions.RequestException as e:
        return {
            "erreur": f"Erreur de requête HTTP: {str(e)}"
        }
    except Exception as e:
        return {
            "erreur": f"Erreur inattendue lors de la requête web: {str(e)}"
        }

# ===== CODE ML EXISTANT (INCHANGÉ) =====

class MLBackend:
    """Backend Machine Learning pour F-IA avec scikit-learn natif"""
    
    def __init__(self):
        self.modeles_entraines = {}
        self.preprocessors = {}
        
    def charger_csv(self, chemin_fichier):
        """Charge un fichier CSV avec pandas"""
        try:
            if not os.path.exists(chemin_fichier):
                raise RuntimeError(f"Fichier non trouvé: {chemin_fichier}")
            df = pd.read_csv(chemin_fichier)
            return df.to_dict('records')  # Retourne une liste de dictionnaires pour F-IA
        except Exception as e:
            raise RuntimeError(f"Erreur lors du chargement CSV: {e}")
    
    def charger_json(self, chemin_fichier):
        """Charge un fichier JSON"""
        try:
            with open(chemin_fichier, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise RuntimeError(f"Erreur lors du chargement JSON: {e}")
    
    def separer_features_target(self, dataset, nom_colonne_target):
        """Sépare features (X) et target (y)"""
        try:
            df = pd.DataFrame(dataset)
            if nom_colonne_target not in df.columns:
                raise RuntimeError(f"Colonne '{nom_colonne_target}' non trouvée")
        
            X = df.drop(columns=[nom_colonne_target])
            y = df[nom_colonne_target]
        
            # CORRECTION: Retourner un dictionnaire au lieu d'un tuple
            return {
                "X": X.values.tolist(),
                "y": y.values.tolist()
            }
        except Exception as e:
            raise RuntimeError(f"Erreur séparation données: {e}")

    
    def standardiser(self, X):
        """Standardise les données (moyenne=0, écart-type=1)"""
        try:
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(np.array(X))
            self.preprocessors['last_scaler'] = scaler
            return X_scaled.tolist()
        except Exception as e:
            raise RuntimeError(f"Erreur standardisation: {e}")
    
    def normaliser(self, X):
        """Normalise les données (entre 0 et 1)"""
        try:
            scaler = MinMaxScaler()
            X_normalized = scaler.fit_transform(np.array(X))
            self.preprocessors['last_normalizer'] = scaler
            return X_normalized.tolist()
        except Exception as e:
            raise RuntimeError(f"Erreur normalisation: {e}")
    
    # === MODÈLES DE CLASSIFICATION ===
    
    def creer_random_forest(self, n_arbres=100, profondeur_max=None):
        """Crée un Random Forest Classifier"""
        try:
            model = RandomForestClassifier(
                n_estimators=n_arbres,
                max_depth=profondeur_max,
                random_state=42
            )
            model_id = f"rf_clf_{len(self.modeles_entraines)}"
            self.modeles_entraines[model_id] = model
            return model_id
        except Exception as e:
            raise RuntimeError(f"Erreur création Random Forest: {e}")
    
    def creer_svm(self, kernel='rbf', C=1.0):
        """Crée un SVM"""
        try:
            model = SVC(kernel=kernel, C=C, random_state=42)
            model_id = f"svm_{len(self.modeles_entraines)}"
            self.modeles_entraines[model_id] = model
            return model_id
        except Exception as e:
            raise RuntimeError(f"Erreur création SVM: {e}")
    
    def creer_knn(self, k=5):
        """Crée un KNN Classifier"""
        try:
            model = KNeighborsClassifier(n_neighbors=k)
            model_id = f"knn_{len(self.modeles_entraines)}"
            self.modeles_entraines[model_id] = model
            return model_id
        except Exception as e:
            raise RuntimeError(f"Erreur création KNN: {e}")
    
    # === MODÈLES DE RÉGRESSION ===
    
    def creer_regression_lineaire(self):
        """Crée une régression linéaire"""
        try:
            model = LinearRegression()
            model_id = f"linreg_{len(self.modeles_entraines)}"
            self.modeles_entraines[model_id] = model
            return model_id
        except Exception as e:
            raise RuntimeError(f"Erreur création régression linéaire: {e}")
    
    def creer_random_forest_reg(self, n_arbres=100, profondeur_max=None):
        """Crée un Random Forest Regressor"""
        try:
            model = RandomForestRegressor(
                n_estimators=n_arbres,
                max_depth=profondeur_max,
                random_state=42
            )
            model_id = f"rf_reg_{len(self.modeles_entraines)}"
            self.modeles_entraines[model_id] = model
            return model_id
        except Exception as e:
            raise RuntimeError(f"Erreur création Random Forest Regressor: {e}")
    
    # === CLUSTERING ===
    
    def creer_kmeans(self, k=3, max_iter=300):
        """Crée un modèle K-Means"""
        try:
            model = KMeans(n_clusters=k, max_iter=max_iter, random_state=42)
            model_id = f"kmeans_{len(self.modeles_entraines)}"
            self.modeles_entraines[model_id] = model
            return model_id
        except Exception as e:
            raise RuntimeError(f"Erreur création K-Means: {e}")
    
    def creer_clustering_hier(self, n_clusters=3):
        """Crée un clustering hiérarchique"""
        try:
            model = AgglomerativeClustering(n_clusters=n_clusters)
            model_id = f"hier_{len(self.modeles_entraines)}"
            self.modeles_entraines[model_id] = model
            return model_id
        except Exception as e:
            raise RuntimeError(f"Erreur création clustering hiérarchique: {e}")
    
    # === ENTRAÎNEMENT ET PRÉDICTION ===
    
    def entrainer_modele(self, model_id, X, y):
        """Entraîne un modèle"""
        try:
            # CORRECTION: Assurer que model_id est une chaîne
            if not isinstance(model_id, str):
                model_id = str(model_id)
            
            if model_id not in self.modeles_entraines:
                raise RuntimeError(f"Modèle '{model_id}' non trouvé. Modèles disponibles: {list(self.modeles_entraines.keys())}")
        
            model = self.modeles_entraines[model_id]
            X_np = np.array(X)
            y_np = np.array(y)
        
            model.fit(X_np, y_np)
            return f"Modèle '{model_id}' entraîné avec succès"
        except Exception as e:
            raise RuntimeError(f"Erreur entraînement: {e}")
    
    def predire(self, model_id, X):
        """Effectue des prédictions"""
        try:
            if model_id not in self.modeles_entraines:
                raise RuntimeError(f"Modèle '{model_id}' non trouvé")
            
            model = self.modeles_entraines[model_id]
            X_np = np.array(X)
            predictions = model.predict(X_np)
            return predictions.tolist()
        except Exception as e:
            raise RuntimeError(f"Erreur prédiction: {e}")
    
    # === ÉVALUATION ===
    
    def evaluer(self, model_id, X, y, metrique='accuracy'):
        """Évalue un modèle avec différentes métriques"""
        try:
            if model_id not in self.modeles_entraines:
                raise RuntimeError(f"Modèle '{model_id}' non trouvé")
            
            model = self.modeles_entraines[model_id]
            X_np = np.array(X)
            y_np = np.array(y)
            
            predictions = model.predict(X_np)
            
            if metrique == 'accuracy':
                return float(accuracy_score(y_np, predictions))
            elif metrique == 'precision':
                precision, _, _, _ = precision_recall_fscore_support(y_np, predictions, average='weighted')
                return float(precision)
            elif metrique == 'recall':
                _, recall, _, _ = precision_recall_fscore_support(y_np, predictions, average='weighted')
                return float(recall)
            elif metrique == 'f1':
                _, _, f1, _ = precision_recall_fscore_support(y_np, predictions, average='weighted')
                return float(f1)
            else:
                raise RuntimeError(f"Métrique '{metrique}' non supportée")
        except Exception as e:
            raise RuntimeError(f"Erreur évaluation: {e}")
    
    def validation_croisee(self, model_id, X, y, nb_plis=5):
        """Validation croisée"""
        try:
            if model_id not in self.modeles_entraines:
                raise RuntimeError(f"Modèle '{model_id}' non trouvé")
            
            model = self.modeles_entraines[model_id]
            X_np = np.array(X)
            y_np = np.array(y)
            
            scores = cross_val_score(model, X_np, y_np, cv=nb_plis)
            return {
                'scores': scores.tolist(),
                'moyenne': float(scores.mean()),
                'ecart_type': float(scores.std())
            }
        except Exception as e:
            raise RuntimeError(f"Erreur validation croisée: {e}")
    
    def matrice_confusion(self, y_true, y_pred):
        """Calcule la matrice de confusion"""
        try:
            y_true_np = np.array(y_true)
            y_pred_np = np.array(y_pred)
            cm = confusion_matrix(y_true_np, y_pred_np)
            return cm.tolist()
        except Exception as e:
            raise RuntimeError(f"Erreur matrice de confusion: {e}")
    
    def rapport_classification(self, y_true, y_pred):
        """Génère un rapport de classification détaillé"""
        try:
            y_true_np = np.array(y_true)
            y_pred_np = np.array(y_pred)
            rapport = classification_report(y_true_np, y_pred_np, output_dict=True)
            return rapport
        except Exception as e:
            raise RuntimeError(f"Erreur rapport de classification: {e}")

# Instance globale du backend ML
ml_backend = MLBackend()

# Fonctions exposées à F-IA (ML + WEB)
def _appeler_python_ml(nom_fonction, args):
    """Interface entre F-IA et le backend ML/Web Python"""
    try:
        # Fonction WEB
        if nom_fonction == "faire_requete_web":
            return faire_requete_web(*args)
        
        # Fonctions ML existantes
        if hasattr(ml_backend, nom_fonction):
            method = getattr(ml_backend, nom_fonction)
            return method(*args)
        else:
            raise RuntimeError(f"Fonction '{nom_fonction}' non trouvée. Fonctions disponibles: {list(dir(ml_backend))}")
    except Exception as e:
        raise RuntimeError(f"Erreur backend: {e}")
