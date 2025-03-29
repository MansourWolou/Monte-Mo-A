Voici un prompt détaillé que vous pouvez utiliser pour demander à un LLM (comme Claude, Grok, ou Gemini) de vous aider à coder cette solution en Python. Ce prompt inclut des détails sur les outils, l'architecture, et la structure du projet pour vous aider à avancer rapidement dans un hackathon :

---

**Prompt pour LLM :**

---

**Objectif :**

Je souhaite développer une application Python qui traite des vidéos en les découpant en segments de 30 secondes, extrait des captures d'écran, et utilise un modèle d'analyse d'image pour obtenir des descriptions. Ces descriptions seront ensuite utilisées pour identifier des parties spécifiques de la vidéo en fonction des requêtes de l'utilisateur via une interface Streamlit.

**Étapes du projet :**

1. **Découpage de la vidéo :**
   - Utiliser un outil comme FFmpeg pour découper la vidéo en segments de 30 secondes.
   - Question : Comment puis-je utiliser FFmpeg en Python pour découper une vidéo en segments de 30 secondes ?

2. **Extraction de captures d'écran :**
   - Extraire 10 captures d'écran de chaque segment vidéo.
   - Question : Quelle est la meilleure façon d'extraire des captures d'écran à partir de segments vidéo en Python ?

3. **Analyse des images :**
   - Envoyer chaque capture d'écran à un modèle d'analyse d'image (par exemple, pixtral-large-latest) pour obtenir un JSON décrivant les éléments présents.
   - Question : Comment puis-je envoyer des images à un modèle d'analyse d'image et traiter les JSON retournés en Python ?

4. **Intégration avec un LLM :**
   - Envoyer les JSON au LLM pour analyse.
   - Question : Comment intégrer ces JSON avec un LLM pour l'analyse ?

5. **Interface utilisateur avec Streamlit :**
   - Créer une interface utilisateur où l'utilisateur peut entrer une requête. Le LLM comparera cette requête avec les descriptions des images pour identifier les parties de la vidéo correspondantes.
   - Question : Comment créer une interface utilisateur avec Streamlit pour interagir avec cette application ?

**Architecture et structure :**

- **Outils :**
  - FFmpeg pour le découpage vidéo.
  - OpenCV pour l'extraction de captures d'écran.
  - Requests ou un autre client HTTP pour envoyer des images au modèle d'analyse d'image.
  - Streamlit pour l'interface utilisateur.

- **Structure du projet :**
  - `video_processor.py` : Script pour découper la vidéo et extraire les captures d'écran.
  - `image_analyzer.py` : Script pour envoyer les images au modèle d'analyse et traiter les JSON.
  - `llm_integration.py` : Script pour intégrer les JSON avec le LLM.
  - `app.py` : Script principal pour l'interface utilisateur Streamlit.

**Exemple de données traitées :**

```python
video_data = {
    "video_id": "video123",
    "title": "Conference XYZ",
    "duration": 3600,
    "segments": [
        {
            "segment_id": 1,
            "start_time": 0,
            "end_time": 30,
            "frames": [
                {
                    "frame_id": 1,
                    "timestamp": 3,
                    "descriptions": [...]  # Résultats Pixtral
                },
                # ... autres frames
            ]
        },
        # ... autres segments
    ]
}
```

---

Ce prompt devrait fournir suffisamment de détails pour que le LLM puisse vous guider à travers le processus de codage de cette solution. Vous pouvez ajuster les détails en fonction des spécificités de votre projet ou des contraintes techniques que vous pourriez avoir.