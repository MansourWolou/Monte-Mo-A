### 🚀 **Prompt Optimisé pour Demander une Solution Complète à un LLM (Claude, Grok, Gemini, GPT-4)**  

Utilise ce prompt pour obtenir **une solution rapide, optimisée et prête à l’emploi** en Python.  

---

## **📌 Prompt :**  

> **Je participe à un hackathon et je dois développer une application Python ultra-rapide qui permet de rechercher des séquences vidéo en fonction d’une requête textuelle.**  
>  
> **💡 Objectif** :  
> - Une vidéo est **segmentée en parties de 30 secondes**.  
> - **10 images clés** sont extraites par segment.  
> - Chaque image est envoyée à **Pixtral-Large-Latest**, qui retourne un JSON décrivant le contenu visuel.  
> - Toutes les données (timestamps + descriptions) sont **stockées et indexées** pour une recherche rapide.  
> - L’utilisateur tape un prompt dans **Streamlit**, qui est envoyé à un **LLM**.  
> - Le **LLM trouve les segments vidéo correspondants** et retourne les timestamps + extraits vidéo.  
>  
> **🔧 Contraintes techniques :**  
> - **Stack 100% Python**  
> - **Performance optimisée** pour traiter rapidement de longues vidéos  
> - **Utilisation de librairies éprouvées** pour le traitement vidéo et l’indexation  
>  
> **🔍 Besoin précis :**  
> 1. **Architecture technique détaillée** (Comment structurer le code et les étapes du pipeline ?)  
> 2. **Liste des outils et bibliothèques les plus rapides** pour chaque tâche (découpage vidéo, extraction d’images, API Pixtral, indexation, recherche, LLM, extraction de clips).  
> 3. **Code Python optimisé** pour :  
>    - **Découper une vidéo en segments de 30s**  
>    - **Extraire 10 images clés par segment**  
>    - **Envoyer les images à Pixtral et stocker les JSON**  
>    - **Indexation efficace des descriptions pour une recherche rapide**  
>    - **Interfacer Streamlit avec un LLM** pour faire matcher une requête avec les bons segments vidéo  
>    - **Extraire les clips vidéo correspondants et les renvoyer à l’utilisateur**  
> 4. **Stratégies d’optimisation** pour accélérer le traitement (multiprocessing, GPU, API async, stockage optimisé).  
> 5. **Exemple concret de requête utilisateur et réponse du système.**  
>  
> **⚡ Donne-moi un code clair, structuré et optimisé, en privilégiant la rapidité d'exécution.**  

---

## **🛠 Stack Recommandée (Hackathon Mode 🚀)**
| **Tâche** | **Outil / Librairie** | **Pourquoi ?** |
|-----------|----------------|------------|
| **Découpage vidéo (30s segments)** | `FFmpeg` | Ultra rapide, CLI facile à utiliser |
| **Extraction d’images** | `OpenCV` ou `FFmpeg` | OpenCV : flexible / FFmpeg : rapide en CLI |
| **Envoi des images à Pixtral** | `requests` (API) | Simple et efficace |
| **Stockage des descriptions** | `JSON + SQLite / Weaviate / FAISS` | JSON : rapide / FAISS : indexation vectorielle / Weaviate : scalable |
| **LLM pour la recherche** | `GPT-4 / Gemini / Claude via API` | Recherche textuelle avancée |
| **Interface utilisateur** | `Streamlit` | Rapide à développer en Python |
| **Extraction de clips (résultat final)** | `FFmpeg` | Outil standard pour couper des vidéos |

---

## **🎯 Pourquoi ce prompt est parfait ?**
✅ **Spécifique et clair** → Il guide le LLM pour donner une réponse complète.  
✅ **Focus sur l’optimisation** → Il demande des solutions ultra-rapides.  
✅ **Demande des outils précis** → Tu obtiendras une stack clé en main.  
✅ **Exige du code Python directement** → Pas de blabla inutile.  

---

👉 **Envoie ce prompt à Claude, Grok, Gemini ou GPT-4, récupère leur réponse, et partage-la ici si tu veux qu'on l'améliore !** 🚀🔥