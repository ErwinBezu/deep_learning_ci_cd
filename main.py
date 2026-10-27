from contextlib import asynccontextmanager
from pathlib import Path
import json
import joblib

from langdetect import detect, DetectorFactory, LangDetectException

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from tensorflow import keras

DOSSIER_MODEL = Path(__file__).resolve().parent / "model"

DetectorFactory.seed = 0

@asynccontextmanager
async def lifespan(app: FastAPI):

    app.state.modele = keras.models.load_model(
        DOSSIER_MODEL / "model.keras"
    )

    app.state.tfidf = joblib.load(
        DOSSIER_MODEL / "vectoriseur.joblib"
    )

    with open(DOSSIER_MODEL / "metrics.json", encoding="utf-8") as f:
        metrics = json.load(f)

    app.state.version = metrics.get("version", "1.0.0")

    yield


app = FastAPI(lifespan=lifespan)

@app.get("/health")
def health():
    return {
        "status": "ok",
        "version": app.state.version
    }

class TexteEntree(BaseModel):
    texte: str

@app.post("/predict")
def predict(donnees: TexteEntree):

    texte = donnees.texte.strip()

    if len(texte) < 64:
        raise HTTPException(
            status_code=400,
            detail="Le texte doit contenir au moins 64 caractères."
        )

    try:
        langue = detect(texte)
    except LangDetectException:
        raise HTTPException(
            status_code=400,
            detail="Impossible de détecter la langue du texte."
        )

    if langue != "en":
        raise HTTPException(
            status_code=400,
            detail=f"Le texte doit être en anglais. Langue détectée : {langue}"
        )

    X = app.state.tfidf.transform([texte]).toarray()

    probabilite = float(
        app.state.modele.predict(X, verbose=0)[0][0]
    )

    classe = int(probabilite >= 0.5)

    categorie = "Horreur" if classe == 1 else "Comédie"

    return {
        "classe": classe,
        "categorie": categorie,
        "probabilite": probabilite if classe == 1 else 1 - probabilite,
        "version": app.state.version
    }

@app.get("/stephan", response_class=HTMLResponse)
def afficher_video():
    return """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Ma vidéo YouTube</title>
        <style>
            body {
                background-color: #121212;
                color: white;
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 40px;
            }

            iframe {
                width: 360px;
                max-width: 100%;
                height: 640px;
                border: none;
                border-radius: 12px;
            }
        </style>
    </head>
    <body>
        <h1>Bienvenue sur mon API !</h1>
        <p>Une petite vidéo pour célébrer mon déploiement Azure !</p>

        <iframe
            src="https://www.youtube.com/embed/FTg_FLt0F9A"
            title="Ma vidéo YouTube Shorts"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
            referrerpolicy="strict-origin-when-cross-origin"
            allowfullscreen>
        </iframe>
    </body>
    </html>
    """

    @app.get("/hello")
def hello():
    return {
        "message": "Hello World !",
        "application": "API de classification de films",
        "version": "2.0.0",
        "environnement": "Azure Container Apps"
    }