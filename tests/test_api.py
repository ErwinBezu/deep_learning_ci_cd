import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert "version" in response.json()


def test_predict_valide(client):
    response = client.post(
        "/predict",
        json={
            "texte": (
                "A group of friends visits an abandoned house "
                "where a mysterious killer begins hunting them."
            )
        }
    )

    assert response.status_code == 200

    resultat = response.json()

    assert resultat["classe"] in [0, 1]
    assert resultat["categorie"] in ["Horreur", "Comédie"]
    assert 0 <= resultat["probabilite"] <= 1
    assert "version" in resultat


def test_predict_invalide(client):
    response = client.post(
        "/predict",
        json={
            "texte": "Bonjour, ceci est un texte français."
        }
    )

    assert response.status_code == 400
    assert "detail" in response.json()


def test_score_minimum():
    chemin = Path(__file__).resolve().parents[1] / "model" / "metrics.json"

    with open(chemin, encoding="utf-8") as f:
        metrics = json.load(f)

    f1 = metrics["metriques"]["f1_test_final"]

    assert f1 >= 0.80, f"F1 insuffisant : {f1:.4f}"