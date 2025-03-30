import os
import subprocess
import json
import argparse
from datetime import datetime

class VideoFrameExtractor:
    def __init__(self, video_path):
        """
        Initialise l'extracteur avec le chemin de la vidéo.
        
        Args:
            video_path (str): Chemin vers le fichier vidéo
        """
        self.video_path = video_path
        self.duration = self.get_video_duration()
        self.frames = []
    
    def get_video_duration(self):
        """
        Obtient la durée totale de la vidéo en secondes en utilisant ffprobe.
        
        Returns:
            float: Durée de la vidéo en secondes
        """
        cmd = [
            "ffprobe", 
            "-v", "error", 
            "-show_entries", "format=duration", 
            "-of", "default=noprint_wrappers=1:nokey=1", 
            self.video_path
        ]
        
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            return float(result.stdout.strip())
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Erreur lors de l'obtention de la durée de la vidéo: {e}")
    
    def extract_frames(self, interval_seconds=1, output_dir=None):
        """
        Extrait une image tous les X secondes de la vidéo.
        
        Args:
            interval_seconds (int): Intervalle en secondes entre chaque image
            output_dir (str, optional): Répertoire de sortie pour les images
            
        Returns:
            list: Liste des chemins vers les images extraites
        """
        # Vérifier si le fichier vidéo existe
        if not os.path.isfile(self.video_path):
            raise FileNotFoundError(f"Le fichier vidéo '{self.video_path}' n'existe pas.")
        
        # Valider l'intervalle
        if interval_seconds < 1:
            print(f"Avertissement: L'intervalle est inférieur à 1 seconde, il a été fixé à 1 seconde.")
            interval_seconds = 1
        elif interval_seconds > self.duration:
            print(f"Avertissement: L'intervalle est supérieur à la durée de la vidéo ({self.duration:.2f}s), il a été fixé à la durée totale.")
            interval_seconds = int(self.duration)
        
        # Créer le répertoire de sortie s'il n'est pas spécifié
        if output_dir is None:
            video_name = os.path.splitext(os.path.basename(self.video_path))[0]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = f"{video_name}_frames_{timestamp}"
        
        # Créer le répertoire s'il n'existe pas
        os.makedirs(output_dir, exist_ok=True)
        
        # Calculer le taux d'images par seconde inverse (1/X)
        fps = 1/interval_seconds
        
        # Définir le modèle de nom pour les images de sortie
        output_pattern = os.path.join(output_dir, "frame_%04d.jpg")
        
        # Construire la commande FFmpeg
        ffmpeg_cmd = [
            "ffmpeg",
            "-i", self.video_path,        # Fichier d'entrée
            "-vf", f"fps={fps}",          # Filtre pour extraire à 1/X fps
            "-q:v", "2",                  # Qualité de l'image (2 est bonne qualité)
            output_pattern                # Modèle de nom pour les fichiers de sortie
        ]
        
        # Exécuter la commande FFmpeg
        try:
            subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"Extraction réussie. Images sauvegardées dans: {output_dir}")
            print(f"Intervalle utilisé: {interval_seconds} secondes (sur une vidéo de {self.duration:.2f} secondes)")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Erreur lors de l'exécution de FFmpeg: {e}\nSortie d'erreur: {e.stderr.decode()}")
        
        # Récupérer la liste des images générées
        self.frames = []
        for file in sorted(os.listdir(output_dir)):
            if file.startswith("frame_") and file.endswith(".jpg"):
                self.frames.append(os.path.join(output_dir, file))
        
        return self.frames
    
    def save_image_paths(self, output_file="image_paths.json"):
        """
        Sauvegarde la liste des chemins d'images dans un fichier JSON.
        
        Args:
            output_file (str): Nom du fichier de sortie
        """
        if not self.frames:
            raise ValueError("Aucune image n'a été extraite. Appelez d'abord extract_frames().")
        
        with open(output_file, 'w') as f:
            json.dump(self.frames, f, indent=4)
        print(f"Liste des chemins d'images sauvegardée dans: {output_file}")
        return output_file

def main():
    parser = argparse.ArgumentParser(description="Extraire des images d'une vidéo à intervalles X secondes")
    parser.add_argument("video", help="Chemin vers le fichier vidéo")
    parser.add_argument("-i", "--interval", type=int, default=1, 
                       help="Intervalle en secondes entre chaque image (défaut: 1, min: 1, max: durée de la vidéo)")
    parser.add_argument("-o", "--output", help="Répertoire de sortie pour les images")
    parser.add_argument("-j", "--json", help="Nom du fichier JSON pour sauvegarder les chemins d'images")
    
    args = parser.parse_args()
    
    try:
        # Créer et utiliser l'extracteur
        extractor = VideoFrameExtractor(args.video)
        image_paths = extractor.extract_frames(args.interval, args.output)
        
        # Sauvegarder ou afficher les résultats
        if args.json:
            extractor.save_image_paths(args.json)
        else:
            print("Liste des chemins d'images:")
            for path in image_paths:
                print(path)
                
    except Exception as e:
        print(f"Erreur: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    main()