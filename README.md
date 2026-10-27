# Classification de résumés de films — CI/CD et déploiement Azure

Projet individuel de mise en production d'un modèle de classification binaire de synopsis de films (**comédie / horreur**). Le projet couvre l'entraînement, l'exposition du modèle par API, les tests, la conteneurisation, l'intégration continue, la publication d'une image dans Azure Container Registry, le déploiement sur Azure Container Apps, un retour arrière et la fin de vie des ressources.

## Technologies

- **Modélisation :** Python, pandas, scikit-learn, TF-IDF, TensorFlow/Keras, KerasTuner et Optuna.
- **API :** FastAPI, Uvicorn, `langdetect`.
- **Qualité et livraison :** pytest, Docker, GitHub Actions, Git.
- **Cloud :** Azure Container Registry (ACR Basic) et Azure Container Apps.
- **Monitoring :** Evidently OSS (rapport HTML local, dérive simulée).

## Résultats du modèle

Le modèle retenu est un réseau de neurones optimisé avec Optuna, utilisant une vectorisation TF-IDF limitée à 5 000 caractéristiques. Les valeurs suivantes proviennent de `metrics.json` :

| Indicateur | Valeur |
|---|---:|
| F1 de validation — Naive Bayes | 0,8618 |
| F1 de validation — réseau initial | 0,8434 |
| F1 de validation — réseau optimisé | 0,8532 |
| **F1 du test final — modèle retenu** | **0,8425** |
| Taille de l'ensemble de test | 469 |
| Seuil de classification | 0,5 |

Les scores de validation servent à comparer les approches ; le score du test final correspond à l'évaluation finale du modèle retenu.

## Organisation du projet

```text
.
├── .github/workflows/ci.yml   # Tests, image Docker et publication ACR
├── data/                      # Données du projet
├── model/                     # model.keras, vectoriseur.joblib, metrics.json
├── monitoring/                # Script de monitoring Evidently
├── notebooks/                 # Entraînement et comparaison des modèles
├── tests/                     # Tests de l'API
├── main.py                    # API FastAPI
├── Dockerfile
├── requirements.txt
├── config.yaml                # Seuils de qualité
├── quality_gate.py            # Vérification des seuils
├── PLAN.md
├── PROCEDURE_MISE_EN_PRODUCTION.md
└── FIN_DE_VIE.md
```

L'arborescence est indicative ; certains fichiers de rapports HTML sont générés à l'exécution.

## Exécution locale

Créer puis activer un environnement virtuel sous PowerShell :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Démarrer l'API :

```powershell
uvicorn main:app --reload
```

Ouvrir `http://127.0.0.1:8000/docs` pour accéder à la documentation interactive. Les routes principales sont :

- `GET /health` : état de l'API et version du modèle ;
- `POST /predict` : classification d'un résumé en anglais et probabilité associée ;
- `GET /docs` : documentation Swagger ;
- `GET /hello` : route ajoutée pour démontrer une nouvelle version et le rollback ;
- `GET /stephan` : page HTML de démonstration.

Le point d'entrée `/predict` applique notamment des contrôles sur la langue et la longueur du texte.

## Tests et barrière qualité

```powershell
pytest -v
python quality_gate.py
```

La barrière qualité vérifie notamment un **F1 final ≥ 0,80** et **au moins 400 exemples de test**, conformément aux seuils définis dans `config.yaml`. En cas d'échec, le déploiement doit être bloqué.

## Docker

```powershell
docker build -t films-api .
docker run --rm -p 8000:8000 films-api
```

L'API est alors accessible sur `http://localhost:8000/docs`.

## Pipeline CI/CD et Azure

Le workflow GitHub Actions comprend trois étapes principales :

1. **`test`** : exécuter les tests et la barrière qualité ;
2. **`image`** : construire et vérifier l'image Docker ;
3. **`publier`** : envoyer l'image vers ACR avec une étiquette basée sur le SHA du commit.

Le déploiement sur **Azure Container Apps** a été réalisé manuellement à partir de l'image publiée dans ACR, avec **1 vCPU et 2 Gio de mémoire**. Les identifiants du registre étaient stockés dans des secrets GitHub associés à l'environnement `Azure_registry`.

Une nouvelle version de l'API a été publiée, puis un **retour arrière vers une image antérieure** a été testé. La procédure et le journal des versions figurent dans `PROCEDURE_MISE_EN_PRODUCTION.md`.

## Monitoring avec Evidently

Un contrôle local de **dérive des données** compare la distribution de caractéristiques de résumés (nombre de caractères et de mots) entre un jeu de référence et un jeu simulant de nouvelles entrées. Le scénario de dérive raccourcit volontairement les textes.

```powershell
python monitoring/monitoring.py
```

Le rapport HTML permet de visualiser les différences de distributions. **Il s'agit d'une démonstration hors ligne**, et non d'un suivi continu de l'API Azure ni d'une mesure de performance sur de nouvelles données étiquetées.

## Estimation des coûts Azure

Dans le cadre du déploiement de mon API de classification de films, j'ai utilisé **Azure Container Registry (offre Basic)** et **Azure Container Apps (1 vCPU, 2 Gio de mémoire)**.

Les coûts réels n'étaient pas visibles depuis mon compte Azure de formation. J'ai donc retenu une méthode d'estimation fondée sur les tarifs publics Azure, la configuration des ressources et leur durée d'utilisation.

### Hypothèses de calcul

Les dates exactes de création et de suppression ainsi que la consommation facturée ne sont pas disponibles. Pour produire une estimation reproductible, je retiens **à titre d'hypothèse** :

- un registre ACR Basic conservé **2 jours** ;
- une application Azure Container Apps en **plan Consommation**, avec **1 réplique**, **1 vCPU et 2 Gio**, représentant au maximum **8 heures d'activité** ;
- un faible nombre de requêtes HTTP, inférieur à l'allocation gratuite ;
- aucun service additionnel payant significatif et pas de dépassement de stockage du registre.

| Ressource | Hypothèse tarifaire indicative (USD, hors taxes) | Calcul | Estimation |
|---|---|---|---:|
| ACR Basic | Environ **0,1666 $/jour** | 2 × 0,1666 | **0,33 $** |
| Container Apps — CPU actif | Environ **0,000024 $/vCPU-seconde** | 1 × 8 × 3 600 × tarif | 0,69 $ avant allocation gratuite |
| Container Apps — mémoire active | Environ **0,000003 $/Gio-seconde** | 2 × 8 × 3 600 × tarif | 0,17 $ avant allocation gratuite |
| Container Apps — après allocation gratuite | 180 000 vCPU-s, 360 000 Gio-s et 2 millions de requêtes gratuites par abonnement et par mois, **si ces quotas restent disponibles** | Consommation supposée sous les quotas | **0,00 $** |
| **Total estimé dans ce scénario** | | ACR + Container Apps après franchise | **≈ 0,33 $ HT** |

**Sans prise en compte des allocations gratuites**, les 8 heures d'activité représenteraient environ **0,86 $** de calcul et mémoire, soit **≈ 1,20 $ HT** avec le registre. Ce montant n'est **pas une facture** : il s'agit d'un scénario illustratif. Le montant réellement dû peut varier selon la région, les répliques actives, les temps d'inactivité, les quotas déjà consommés par l'abonnement partagé, les services annexes et la durée réelle d'existence des ressources. Une réplique conservée active ou inactive plus longtemps modifierait notamment le calcul.

Sources : [Microsoft — Facturation Azure Container Apps](https://learn.microsoft.com/fr-fr/azure/container-apps/billing), [Microsoft — Tarification Azure Container Registry](https://azure.microsoft.com/fr-fr/pricing/details/container-registry/), [Microsoft — Calculateur Azure](https://azure.microsoft.com/fr-fr/pricing/calculator/). Les montants unitaires sont des **ordres de grandeur indicatifs**, non des tarifs contractuels vérifiés pour l'abonnement de formation.

## Fin de vie et nettoyage

À la fin de l'exercice, le **groupe de ressources Azure a été supprimé**, entraînant la suppression des ressources qu'il contenait. Cette méthode diffère de la procédure initiale qui prévoyait la suppression individuelle de l'application, de son environnement et du registre. Elle n'est appropriée que si le groupe n'était pas partagé ; sinon, l'incident doit être signalé au responsable de l'abonnement.

La confirmation de la suppression effective et les captures justificatives doivent être conservées pour le rendu. Les fichiers locaux et le dépôt Git restent disponibles pour l'évaluation. Voir `FIN_DE_VIE.md`.

## Documents de suivi

- [`PLAN.md`](PLAN.md) : planification initiale et bilan des tâches ;
- [`PROCEDURE_MISE_EN_PRODUCTION.md`](PROCEDURE_MISE_EN_PRODUCTION.md) : déploiement, contrôles et rollback ;
- [`FIN_DE_VIE.md`](FIN_DE_VIE.md) : stratégie de retrait, coûts et preuves de nettoyage.
