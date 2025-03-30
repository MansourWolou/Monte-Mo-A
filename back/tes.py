import requests
import numpy as np
import torch
import pandas as pd
import os
import json
import time
from datetime import datetime
from moviepy.editor import VideoFileClip
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration, pipeline, WhisperProcessor, WhisperForConditionalGeneration

class DescripteurVideoAutomatique:
    def __init__(self, intervalle=5, top_n=10, utiliser_cuda=True):
        self.intervalle = intervalle
        self.top_n = top_n
        self.utiliser_cuda = utiliser_cuda
        self.device = "cuda" if utiliser_cuda and torch.cuda.is_available() else "cpu"
        self.chemin_video = None
        self.scenes = []
        self.descriptions = []
        self.api_key_mistral = "JpPD7Mcbkn4kt9EASK8FyXKT0s8zdNn5"
        self.bibliotheque_path = "bibliotheque_videos.json"

    def generer_nom_descriptif(self, legendes, transcriptions):
        """Génère un nom descriptif à partir des légendes et transcriptions"""
        # Combinaison des 3 premières légendes
        nom_base = " - ".join([leg.split(".")[0] for leg in legendes[:3] if leg])
        # Limiter la longueur du nom
        if not nom_base:
            nom_base = "Vidéo sans description"
        return nom_base[:50] + "..." if len(nom_base) > 50 else nom_base

    def charger_modele(self):
        print("📦 Chargement des modèles...")
        # Modèle BLIP pour la description d'images
        self.processeur = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
        self.modele = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large").to(self.device)


        # Modèle Whisper pour la transcription audio
        self.whisper_processor = WhisperProcessor.from_pretrained("openai/whisper-small")
        self.whisper_model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small").to(self.device)

        # Traducteur
        self.traducteur = pipeline("translation_en_to_fr", model="Helsinki-NLP/opus-mt-en-fr")
        print("✅ Modèles chargés avec succès!")

    def extraire_scenes(self):
        clip = VideoFileClip(self.chemin_video)
        duree = clip.duration
        self.scenes = [(debut, min(debut + self.intervalle, duree)) for debut in range(0, int(duree), self.intervalle)]

    def obtenir_image_milieu(self, debut, fin):
        clip = VideoFileClip(self.chemin_video).subclip(debut, fin)
        image = clip.get_frame((fin - debut) / 2)
        return Image.fromarray(image)

    def generer_legende(self, image):
        inputs = self.processeur(image, return_tensors="pt").to(self.device)
        sortie = self.modele.generate(**inputs)
        legende_en = self.processeur.decode(sortie[0], skip_special_tokens=True)
        legende_fr = self.traducteur(legende_en)[0]['translation_text']
        return legende_fr

    def extraire_audio(self, debut, fin, nom="scene_audio.wav"):
        try:
            clip = VideoFileClip(self.chemin_video).subclip(debut, fin)
            if clip.audio is not None:
                audio_path = os.path.join(os.getcwd(), nom)
                clip.audio.write_audiofile(audio_path, logger=None)
                return audio_path
            else:
                print(f"Avertissement: Pas d'audio dans la section {debut}-{fin}")
                return None
        except Exception as e:
            print(f"Erreur d'extraction audio: {str(e)}")
            return None

    def transcrire_audio_whisper(self, audio_path):
        if audio_path is None:
            return "Pas d'audio disponible pour cette section."

        try:
            import librosa
            import soundfile as sf

            # Chargement de l'audio
            audio, rate = librosa.load(audio_path, sr=16000)

            # Convertir en format attendu par Whisper
            input_features = self.whisper_processor(audio, sampling_rate=16000, return_tensors="pt").input_features.to(self.device)

            # Générer les tokens de prédiction
            predicted_ids = self.whisper_model.generate(input_features, language="fr", task="transcribe")

            # Décodage de la transcription
            transcription = self.whisper_processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]

            if not transcription:
                return "Aucune transcription détectée."

            return transcription

        except Exception as e:
            return f"Erreur de transcription Whisper: {str(e)}"
        finally:
            # Nettoyage du fichier
            try:
                if os.path.exists(audio_path):
                    os.remove(audio_path)
            except:
                pass

    def demander_a_mistral(self, prompt, contexte=""):
        url = "https://api.mistral.ai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key_mistral}",
            "Content-Type": "application/json"
        }

        messages = [
            {"role": "system", "content": "Vous êtes un assistant spécialisé dans l'analyse vidéo. Répondez en français."},
            {"role": "user", "content": f"Contexte sur la vidéo: {contexte}\n\nQuestion: {prompt}"}
        ]

        data = {
            "model": "mistral-large-latest",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 800
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Erreur lors de la communication avec Mistral: {str(e)}"

    def decrire_video(self):
        self.extraire_scenes()
        self.descriptions = []

        for debut, fin in self.scenes:
            print(f"Analyse de la scène {self.formater_temps(debut)}-{self.formater_temps(fin)}...")

            # Génération de la légende visuelle
            image = self.obtenir_image_milieu(debut, fin)
            legende = self.generer_legende(image)

            # Extraction et transcription audio avec Whisper
            audio_path = self.extraire_audio(debut, fin, nom=f"audio_{int(debut)}.wav")
            transcription = self.transcrire_audio_whisper(audio_path)

            # Calcul du score (pondération ajustée pour favoriser les scènes avec audio)
            score = len(legende) * 0.05 + len(transcription) * 0.15 + np.random.rand() * 0.3

            self.descriptions.append({
                "debut": debut,
                "fin": fin,
                "legende": legende,
                "transcription": transcription,
                "score": score
            })

    def obtenir_meilleures_scenes(self):
        return sorted(self.descriptions, key=lambda x: x["score"], reverse=True)[:self.top_n]

    def formater_temps(self, secondes):
        return f"{int(secondes // 60):02d}:{int(secondes % 60):02d}"

    def trouver_moment_interessant(self, scenes):
        if not scenes:
            return "Aucun moment intéressant trouvé"

        top = max(scenes, key=lambda x: x["score"])
        return f"Le moment le plus intéressant se trouve entre {self.formater_temps(top['debut'])} et {self.formater_temps(top['fin'])}"

    def analyser_video(self, video_path, nom_personnalise=None):
        if not video_path:
            return None, "Veuillez télécharger une vidéo.", None

        # Sauvegarde du chemin de la vidéo
        self.chemin_video = video_path

        # Chargement du modèle si nécessaire
        if not hasattr(self, 'modele') or not hasattr(self, 'whisper_model'):
            self.charger_modele()

        # Analyse de la vidéo
        try:
            self.decrire_video()
            meilleures_scenes = self.obtenir_meilleures_scenes()
            moment_interessant = self.trouver_moment_interessant(meilleures_scenes)

            # Création d'un DataFrame pour l'affichage
            df = pd.DataFrame([{
                "Rang": i+1,
                "Début": self.formater_temps(s["debut"]),
                "Fin": self.formater_temps(s["fin"]),
                "Description": s["legende"],
                "Transcription audio": s["transcription"]
            } for i, s in enumerate(meilleures_scenes)])

            # Obtenir le nom de fichier de la vidéo pour l'affichage
            nom_fichier = os.path.basename(video_path)

            # Ajout à la bibliothèque
            bibliotheque_mise_a_jour = self.ajouter_a_bibliotheque(video_path, self.descriptions, nom_personnalise)

            return df, f"Vidéo: {nom_fichier}\n{moment_interessant}", bibliotheque_mise_a_jour

        except Exception as e:
            return None, f"Erreur lors de l'analyse: {str(e)}", None

    def analyser_et_demander(self, video_path, prompt, nom_personnalise=None):
        df, message, bibliotheque = self.analyser_video(video_path, nom_personnalise)

        if df is None:
            return None, message, None, bibliotheque

        # Préparation du contexte pour Mistral
        contexte = "Informations sur les scènes principales: "
        for i, row in df.head(3).iterrows():
            contexte += f"\nScène {row['Début']}-{row['Fin']}: {row['Description']}. Audio: {row['Transcription audio']}"

        # Interrogation de Mistral
        reponse_mistral = self.demander_a_mistral(prompt, contexte)

        return df, message, reponse_mistral, bibliotheque
    

if __name__ == "__main__":
    # Initialize the analyzer
    descripteur = DescripteurVideoAutomatique()

    