Voici un **prompt ultra-optimisé** pour ton hackathon, avec **outils "fast & furious"** et une **architecture clé en main** :

---

### 🚀 **Prompt pour LLM (Claude/Gemini/Grok)**  
```markdown
Je participe à un hackathon et dois coder en Python un moteur de recherche vidéo avec cette architecture :

**📌 Objectif**  
Identifier les segments vidéo correspondant à une requête utilisateur (ex: "Montre-moi les slides avec des graphiques") en analysant des frames.

**🔥 Stack "Speed Overkill" demandée** :  
1. **Découpage vidéo** :  
   - Outil : `ffmpeg-python` (car FFmpeg est 10x plus rapide que MoviePy)  
   - Commande : Découper la vidéo en segments de 30s + extraire 10 frames/segment  
   ```python
   # Exemple de commande FFmpeg pour extraire 10 frames uniformément réparties
   ffmpeg -i input.mp4 -vf fps=1/3 thumbnails_%03d.jpg
   ```

2. **Analyse d'images** :  
   - Modèle : `pixstral-large-latest` via API (ou `CLIP` + `LLaVA` en local si API trop lente)  
   - Format de sortie :  
   ```json
   {
     "objects": [{"label": "car", "confidence": 0.92}],
     "text": "Panneau STOP visible",
     "action": "person walking"
   }
   ```

3. **Stockage** :  
   - Structure de données :  
   ```python
   video_data = {
     "segments": [
       {
         "start": 0, 
         "end": 30,
         "frames": [
           {"time": 3.1, "text": "Slide: Market Growth 2023", "tags": ["chart", "blue"]},
           # ...
         ]
       }
     ]
   }
   ```
   - DB : `DuckDB` (pour du SQL ultra-rapide sur fichier) ou `FAISS` si recherche vectorielle

4. **Recherche** :  
   - LLM : `Claude 3 Haiku` (rapide et pas cher) avec prompt structuré :  
   ```python
   prompt = f"""
   Compare la requête "{user_query}" avec ces descriptions vidéo :
   {video_data}

   Retourne UNIQUEMENT les timestamps [start,end] des segments pertinents, triés par pertinence.
   """
   ```

5. **Front** :  
   - `Streamlit` avec :  
   ```python
   import streamlit as st
   st.video(highlighted_segment_path)
   ```

**🎯 Demande** :  
1. Donne-moi le code Python complet le plus optimisé possible  
2. Focus sur :  
   - Parallélisation avec `asyncio` pour l'analyse des frames  
   - Cache des résultats (éviter de réanalyser 2x la même vidéo)  
3. Propose un fallback si pixstral est trop lent (ex: YOLOv8 + OCR)  

**⏱️ Contraintes Hackathon** :  
- Temps limité → Privilégier les outils avec API simples  
- Pas d'infra cloud → Tout doit tourner en local  
```  

---

### 🛠️ **Outils "Gagne-Temps" Recommandés**  
1. **Découpage vidéo** :  
   - `ffmpeg-python` (wrap FFmpeg) > MoviePy pour la vitesse  
   - Alternative : `PyAV` (bindings Python pour FFmpeg)  

2. **Extraction de frames** :  
   - `OpenCV` (`cv2.VideoCapture`) pour du traitement batch rapide  

3. **Analyse d'images** :  
   - API la plus rapide : `Replicate` (pour pixstral)  
   - Local : `LLaVA-1.6` (modèle 7B quantisé) + `CLIP`  

4. **Recherche** :  
   - Pour du texte : `TF-IDF` + `scikit-learn` (simple)  
   - Pour du vectoriel : `FAISS` (local) > Pinecone  

5. **LLM** :  
   - Claude Haiku : 3x plus rapide que GPT-4 pour ce cas  

---

### 📂 **Structure de Fichiers Recommandée**  
```bash
.
├── app.py                  # Streamlit front
├── video_processor.py      # Découpage + extraction
├── analyzer.py             # Appel à pixstral/LLaVA
├── search.py               # Recherche LLM + ranking
└── cache/                  # Stockage des JSON analysés
```

---

### ⚡ **Astuce Hackathon**  
Utilise ce snippet pour paralléliser l'analyse des frames :  
```python
from concurrent.futures import ThreadPoolExecutor

def analyze_frame(frame_path):
    # Appel à pixstral ici
    return description

with ThreadPoolExecutor(max_workers=8) as executor:
    results = list(executor.map(analyze_frame, frame_paths))
```

Avec ce prompt, tu devrais obtenir un code prêt à l'emploi en quelques minutes ! 🚀