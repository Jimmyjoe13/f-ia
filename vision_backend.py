# vision_backend.py - Backend Vision par Ordinateur pour F-IA Phase 3
import cv2
import numpy as np
import os
import uuid
from errors import RuntimeError

class VisionBackend:
    """Backend Vision pour F-IA utilisant OpenCV"""

    def __init__(self):
        # Stockage des images en mémoire : { "img_uuid": numpy_array }
        self.images = {}

    def _generer_id(self):
        return f"img_{uuid.uuid4().hex[:8]}"

    def _recuperer_image(self, image_id):
        if image_id not in self.images:
            raise RuntimeError(f"Image introuvable : {image_id}")
        return self.images[image_id]

    def _stocker_image(self, img_array):
        img_id = self._generer_id()
        self.images[img_id] = img_array
        return img_id

    # === CHARGEMENT / SAUVEGARDE ===

    def charger_image(self, chemin_fichier):
        """Charge une image depuis un fichier"""
        try:
            if not os.path.exists(chemin_fichier):
                raise RuntimeError(f"Fichier image non trouvé : {chemin_fichier}")

            img = cv2.imread(chemin_fichier)
            if img is None:
                raise RuntimeError(f"Impossible de lire l'image : {chemin_fichier}")

            return self._stocker_image(img)
        except Exception as e:
            raise RuntimeError(f"Erreur charger_image : {e}")

    def sauvegarder_image(self, image_id, chemin_sortie):
        """Sauvegarde une image sur le disque"""
        try:
            img = self._recuperer_image(image_id)
            succes = cv2.imwrite(chemin_sortie, img)
            if not succes:
                raise RuntimeError(f"Échec de la sauvegarde vers {chemin_sortie}")
            return True
        except Exception as e:
            raise RuntimeError(f"Erreur sauvegarder_image : {e}")

    # === TRANSFORMATIONS ===

    def redimensionner(self, image_id, largeur, hauteur):
        """Redimensionne l'image"""
        try:
            img = self._recuperer_image(image_id)
            # Conversion en entier pour éviter les erreurs
            w, h = int(largeur), int(hauteur)
            resized = cv2.resize(img, (w, h))
            return self._stocker_image(resized)
        except Exception as e:
            raise RuntimeError(f"Erreur redimensionner : {e}")

    def rotation(self, image_id, angle):
        """Effectue une rotation de l'image"""
        try:
            img = self._recuperer_image(image_id)
            (h, w) = img.shape[:2]
            centre = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(centre, float(angle), 1.0)
            rotated = cv2.warpAffine(img, M, (w, h))
            return self._stocker_image(rotated)
        except Exception as e:
            raise RuntimeError(f"Erreur rotation : {e}")

    def inverser_couleurs(self, image_id):
        """Inverse les couleurs (négatif)"""
        try:
            img = self._recuperer_image(image_id)
            inverted = cv2.bitwise_not(img)
            return self._stocker_image(inverted)
        except Exception as e:
            raise RuntimeError(f"Erreur inverser_couleurs : {e}")

    # === FILTRES ===

    def filtre_flou(self, image_id, intensite):
        """Applique un flou gaussien"""
        try:
            img = self._recuperer_image(image_id)
            k = int(intensite)
            if k % 2 == 0: k += 1 # Le noyau doit être impair
            blurred = cv2.GaussianBlur(img, (k, k), 0)
            return self._stocker_image(blurred)
        except Exception as e:
            raise RuntimeError(f"Erreur filtre_flou : {e}")

    def filtre_sepia(self, image_id):
        """Applique un filtre sépia"""
        try:
            img = self._recuperer_image(image_id)
            img_float = np.array(img, dtype=np.float64)
            img_sepia = cv2.transform(img_float, np.matrix([[0.272, 0.534, 0.131],
                                                            [0.349, 0.686, 0.168],
                                                            [0.393, 0.769, 0.189]]))
            img_sepia = np.clip(img_sepia, 0, 255)
            return self._stocker_image(np.array(img_sepia, dtype=np.uint8))
        except Exception as e:
            raise RuntimeError(f"Erreur filtre_sepia : {e}")

    def niveau_gris(self, image_id):
        """Convertit en niveaux de gris"""
        try:
            img = self._recuperer_image(image_id)
            if len(img.shape) == 2: # Déjà gris
                return self._stocker_image(img.copy())
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            return self._stocker_image(gray)
        except Exception as e:
            raise RuntimeError(f"Erreur niveau_gris : {e}")

    # === DÉTECTION ===

    def detecter_contours(self, image_id):
        """Détecte les contours (Canny) et retourne une image avec les contours dessinés"""
        try:
            img = self._recuperer_image(image_id)
            # Convertir en gris si nécessaire
            if len(img.shape) == 3:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            else:
                gray = img

            edges = cv2.Canny(gray, 100, 200)

            # On retourne l'image des contours (noir et blanc)
            # Ou on pourrait dessiner sur l'original ?
            # Pour l'instant, retournons l'image binaire des edges
            return self._stocker_image(edges)
        except Exception as e:
            raise RuntimeError(f"Erreur detecter_contours : {e}")

    def detecter_visages(self, image_id):
        """Détecte les visages et retourne une liste de rectangles [x, y, w, h]"""
        try:
            img = self._recuperer_image(image_id)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Chargement du classifieur Haar
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            face_cascade = cv2.CascadeClassifier(cascade_path)

            if face_cascade.empty():
                 raise RuntimeError("Impossible de charger le modèle de détection de visage (haarcascade)")

            faces = face_cascade.detectMultiScale(gray, 1.1, 4)

            # Retourner une liste de dictionnaires ou de listes
            resultat = []
            for (x, y, w, h) in faces:
                resultat.append([int(x), int(y), int(w), int(h)])

            return resultat
        except Exception as e:
            raise RuntimeError(f"Erreur detecter_visages : {e}")

    # === ANALYSE ===

    def dimensions(self, image_id):
        """Retourne [largeur, hauteur]"""
        try:
            img = self._recuperer_image(image_id)
            h, w = img.shape[:2]
            return [w, h]
        except Exception as e:
            raise RuntimeError(f"Erreur dimensions : {e}")

    def histogramme(self, image_id):
        """Retourne un histogramme simplifié (moyenne par canal B, G, R)"""
        try:
            img = self._recuperer_image(image_id)
            if len(img.shape) == 2:
                # Gris
                hist = cv2.calcHist([img], [0], None, [256], [0, 256])
                return hist.flatten().tolist()
            else:
                # Couleur : on va simplifier pour l'instant et retourner les moyennes
                # Ou retourner 3 listes ? F-IA gère les listes de listes ? Oui.
                colors = ('b', 'g', 'r')
                res = {}
                for i, color in enumerate(colors):
                    hist = cv2.calcHist([img], [i], None, [256], [0, 256])
                    res[color] = hist.flatten().tolist()
                return res
        except Exception as e:
            raise RuntimeError(f"Erreur histogramme : {e}")

    def luminosite_moyenne(self, image_id):
        """Retourne la luminosité moyenne de l'image"""
        try:
            img = self._recuperer_image(image_id)
            if len(img.shape) == 3:
                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                # Canal V est le 3ème (index 2)
                return float(np.mean(hsv[:,:,2]))
            else:
                return float(np.mean(img))
        except Exception as e:
            raise RuntimeError(f"Erreur luminosite_moyenne : {e}")

# Instance globale
vision_backend = VisionBackend()

def _appeler_python_vision(nom_fonction, args):
    """Interface d'appel pour le builtin.py"""
    try:
        if hasattr(vision_backend, nom_fonction):
            method = getattr(vision_backend, nom_fonction)
            return method(*args)
        else:
            raise RuntimeError(f"Fonction vision inconnue : {nom_fonction}")
    except Exception as e:
        raise RuntimeError(f"Erreur VisionBackend : {e}")
