import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from ml_backend import ml_backend

class TestMLBackend(unittest.TestCase):
    def setUp(self):
        """Initialise un backend ML propre pour chaque test"""
        # Reset des modèles pour éviter les conflits entre tests
        ml_backend.modeles_entraines.clear()
        ml_backend.preprocessors.clear()

    def test_create_and_train_rf(self):
        """Test création et entraînement Random Forest"""
        X = [[1, 2], [2, 3], [3, 1], [4, 5], [5, 4], [6, 2]]
        y = [0, 0, 0, 1, 1, 0]
        
        # Créer le modèle
        model_id = ml_backend.creer_random_forest(50, 5)
        self.assertIsInstance(model_id, str)
        self.assertTrue(model_id.startswith("rf_clf_"))
        
        # Entraîner le modèle
        res = ml_backend.entrainer_modele(model_id, X, y)
        self.assertIn("entraîné", res)
        self.assertIn("succès", res)
        
        # Tester prédictions
        preds = ml_backend.predire(model_id, [[2.5, 2.5], [6, 3]])
        self.assertEqual(len(preds), 2)
        # Vérifier que les prédictions sont des entiers (0 ou 1)
        for pred in preds:
            self.assertIn(pred, [0, 1])

    def test_split_features_target(self):
        """Test séparation features/target"""
        dataset = [
            {"a": 1, "b": 2, "label": 0},
            {"a": 2, "b": 3, "label": 1}
        ]
        
        split = ml_backend.separer_features_target(dataset, "label")
        
        # Vérifier la structure de retour
        self.assertIn("X", split)
        self.assertIn("y", split)
        
        X = split["X"]
        y = split["y"]
        
        # Vérifier les dimensions
        self.assertEqual(len(X), 2)
        self.assertEqual(len(y), 2)
        self.assertEqual(len(X[0]), 2)  # 2 features (a, b)
        
        # Vérifier les valeurs
        self.assertEqual(X[0], [1, 2])
        self.assertEqual(X[1], [2, 3])
        self.assertEqual(y[0], 0)
        self.assertEqual(y[1], 1)

    def test_preprocessing(self):
        """Test standardisation et normalisation"""
        X = [[1, 2], [3, 4], [5, 6]]
        
        # Test standardisation
        X_std = ml_backend.standardiser(X)
        self.assertEqual(len(X_std), 3)
        self.assertEqual(len(X_std[0]), 2)
        
        # Test normalisation
        X_norm = ml_backend.normaliser(X)
        self.assertEqual(len(X_norm), 3)
        self.assertEqual(len(X_norm[0]), 2)
        
        # Vérifier que la normalisation donne des valeurs entre 0 et 1
        for row in X_norm:
            for val in row:
                self.assertGreaterEqual(val, 0.0)
                self.assertLessEqual(val, 1.0)

    def test_evaluation(self):
        """Test évaluation de modèle"""
        X = [[1, 2], [2, 3], [3, 1], [4, 5], [5, 4], [6, 2]]
        y = [0, 0, 0, 1, 1, 0]
        
        # Créer et entraîner modèle
        model_id = ml_backend.creer_random_forest(10, 3)
        ml_backend.entrainer_modele(model_id, X, y)
        
        # Évaluer
        score = ml_backend.evaluer(model_id, X, y, "accuracy")
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)

if __name__ == "__main__":
    unittest.main()
