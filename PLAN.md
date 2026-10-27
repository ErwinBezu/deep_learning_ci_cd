# Planification du projet de mise en production d'un modèle

## 1. Contexte et objectifs
**Projet** : classifier des résumés de films en deux catégories (horreur / comédie), comparer plusieurs modèles, exposer le meilleur via une API FastAPI, automatiser les vérifications et la construction Docker avec GitHub Actions, puis déployer manuellement sur Azure et démontrer un retour arrière.

**Cadre** : projet individuel, compétence C12 « Planifier le projet ». Hypothèse de planification : 5 jours de 7 h, soit 35 h disponibles, à confirmer avec le formateur. Les dates calendaires ne sont pas fournies : J1 à J5 désignent les cinq jours de travail. Les charges estimées sont des objectifs de planification, non des durées garanties.

**Livrables C12** : `PLAN.md`, `PROCEDURE_MISE_EN_PRODUCTION.md` (avec journal des versions), `FIN_DE_VIE.md`, preuves de fin de vie et bilan prévu/réel dans la fiche finale.

## 2. Ressources mobilisées
- **Humaines** : 1 apprenant (réalisation, tests, décisions et déploiement) ; formateur (validation et assistance ponctuelle).
- **Matérielles** : ordinateur personnel ou de formation, connexion Internet.
- **Techniques** : Python, venv, VS Code, Jupyter, pandas, scikit-learn, TensorFlow/Keras, KerasTuner, Optuna, joblib, FastAPI, pytest, Docker, Git/GitHub, GitHub Actions, Azure Container Registry (Basic), Azure Container Apps.
- **Financières** : outils locaux généralement gratuits ; ressources Azure susceptibles d'être facturées (registre et application). Budget réel non communiqué : contrôler les estimations et supprimer les ressources à la fin. Ne pas supposer un coût nul.

## 3. Tableau de planification

Les durées sont des **estimations initiales**. La colonne « Charge réelle » contient ici des **repères horodatés reconstitués à partir des échanges**, et non des durées chronométrées : les messages ne permettent pas de mesurer les interruptions ou le travail hors conversation. Les numéros T servent à repérer les dépendances.

| ID | Tâche | Dépend de | Charge estimée | Suivi reconstitué (horodatages) | Ressources (H / M / T / F) | Date prévue |
|---|---|---|---:|---|---|---|
| T01 | C12 : préparer PLAN, procédure et plan de fin de vie (versions initiales) | — | 1 h 30 | 22/10, 09 h 05 — documents C12 préparés | Apprenant / PC / Markdown, VS Code / 0 € hors équipement | J1 |
| T02 | Préparer dépôt, venv, notebook et dépendances | T01 | 0 h 30 | 22/10, avant 12 h 46 — environnement prêt pour le notebook (heure exacte inconnue) | Apprenant / PC / Python, Git, Jupyter / 0 € | J1 |
| T03 | Audit, nettoyage et dédoublonnage des données | T02 | 1 h | 22/10, 12 h 46 — audit des données en cours | Apprenant / PC / pandas / 0 € | J1 |
| T04 | Découpage stratifié 60 % / 20 % / 20 % | T03 | 0 h 45 | 22/10, 13 h 17 — étape du découpage abordée | Apprenant / PC / scikit-learn / 0 € | J1 |
| T05 | TF-IDF appris sur l'entraînement uniquement | T04 | 0 h 45 | 22–26/10 — TF-IDF réalisé, plage non isolable | Apprenant / PC / scikit-learn / 0 € | J1 |
| T06 | Baselines : logistique, Bayes naïf, réseau simple, 5 graines et marge de bruit | T05 | 2 h 30 | 22–26/10 — baselines réalisées, plage non isolable | Apprenant / PC / scikit-learn, Keras / 0 € | J1–J2 |
| T07 | KerasTuner : fonction de construction, 20 essais | T06 | 2 h 30 | 22–26/10 — optimisation KerasTuner, plage non isolable | Apprenant / PC / KerasTuner, TensorFlow / 0 € | J2 |
| T08 | Optuna : mêmes paramètres et 20 essais ; comparaison | T07 | 2 h | 22–26/10 — optimisation Optuna, plage non isolable | Apprenant / PC / Optuna / 0 € | J2 |
| T09 | Verdict : 5 graines, comparaison, test final unique | T08 | 1 h 30 | 22–26/10 — verdict final, plage non isolable | Apprenant / PC / Keras, scikit-learn / 0 € | J2–J3 |
| T10 | Sauvegarder modèle, TF-IDF, metrics.json et échantillon de référence | T09 | 1 h | Au plus tard le 26/10 — artefacts du modèle disponibles | Apprenant / PC / Keras, joblib, JSON / 0 € | J3 |
| T11 | FastAPI : /health et /predict, validation et essais manuels | T10 | 2 h | 26/10, dès 09 h 41 — travail sur FastAPI | Apprenant / PC / FastAPI, uvicorn / 0 € | J3 |
| T12 | Tests automatiques de l'API et du score minimum | T11 | 1 h | 26/10, 12 h 23 — 4 tests pytest réussis | Apprenant / PC / pytest, TestClient / 0 € | J3 |
| T13 | Barrière qualité : config.yaml, script, acceptation et rejet simulé | T10, T12 | 1 h | 26/10 — barrière qualité mise en place, heure non isolable | Apprenant / PC / Python, YAML / 0 € | J3 |
| T14 | Dockerfile et .dockerignore ; construction, taille et essais du conteneur | T11–T13 | 2 h | 26/10, 14 h 54 — conteneur Docker lancé | Apprenant / PC / Docker / 0 € local | J3–J4 |
| T15 | GitHub Actions : jobs test et image, vérification verte | T14 | 1 h 30 | 26/10, dès 15 h 13 — GitHub Actions abordé | Apprenant / PC / GitHub Actions / Selon quotas GitHub | J4 |
| T16 | Démontrer l'échec du seuil impossible puis rétablir le vert | T15 | 0 h 30 | 26–27/10 — contrôle du seuil, heure non isolable | Apprenant / PC / GitHub Actions / Selon quotas | J4 |
| T17 | Créer Azure Container Registry Basic et secrets GitHub | T16 | 1 h | 27/10, dès 09 h 09 — travaux Azure et ACR | Apprenant / PC / Azure, GitHub / Azure facturable | J4 |
| T18 | Ajouter le job publier ; pousser l'image étiquetée par commit | T17 | 1 h | 27/10 — publication vers ACR, heure non isolable | Apprenant / PC / GitHub Actions, ACR / Azure facturable | J4 |
| T19 | Déployer manuellement Azure Container Apps et tester l'adresse publique | T18 | 1 h 30 | 27/10 — déploiement Azure Container Apps | Apprenant / PC / Azure Container Apps / Azure facturable | J5 |
| T20 | Ajouter /hello, publier une nouvelle image et redéployer | T19 | 1 h | 27/10 — nouvelle version /hello déployée | Apprenant / PC / FastAPI, GitHub, Azure / Azure facturable | J5 |
| T21 | Retour arrière vers le commit précédent ; preuves | T20 | 0 h 45 | 27/10 — retour arrière testé | Apprenant / PC / Azure, Git / Azure facturable | J5 |
| T22 | Fin de vie : relever coûts, supprimer application, environnement et registre ; preuves | T21 | 1 h | 27/10, 16 h 17 — suppression du groupe annoncée ; coût non visible | Apprenant / PC / Portail Azure / Facturation jusqu'à suppression | J5 |
| T23 | Finaliser C12, README, journal des versions, bilan prévu/réel et fiche finale | T22 | 1 h 45 | 27/10, à partir de 16 h 14 — mise à jour des documents C12 | Apprenant / PC / Markdown, Git / 0 € hors équipement | J5 |
| | **TOTAL** | | **32 h 15** | **Durée totale réelle non mesurable** | | **J1–J5** |

**Marge de sécurité : 2 h 45** sur les 35 h disponibles. À utiliser en priorité pour les essais KerasTuner/Optuna, les erreurs Docker ou les permissions Azure. Si une tâche dépasse son estimation, noter l'écart au lieu de modifier rétroactivement l'estimation initiale.

## 4. Jalons et critères de validation

| Jalon | Échéance cible | Critère de validation / preuve |
|---|---|---|
| M1 | J1 | C12 initial rédigé, données nettoyées et séparées, TF-IDF sans fuite |
| M2 | J2 | Baselines et recherches KerasTuner/Optuna comparées |
| M3 | J3 | Notebook exécutable, dossier `model/` complet, API et tests réussis |
| M4 | J4 | Image Docker testée, CI verte puis rouge volontairement puis verte, image publiée dans ACR |
| M5 | J5 | API Azure publique testée, ajout /hello, retour arrière vérifié |
| M6 | J5 | Ressources Azure supprimées, coûts relevés, livrables et preuves finalisés |

## 5. Risques et réponses prévues

| Risque | Conséquence | Mesure préventive / corrective |
|---|---|---|
| Entraînements et 40 essais d'optimisation longs | Dépassement du planning | Tester le code sur un petit essai, puis lancer les 20 + 20 essais demandés ; utiliser la marge de sécurité |
| Fuite de données ou doublons | Score artificiellement élevé | Dédoublonner avant séparation ; ajuster le TF-IDF sur l'entraînement seulement ; ne tester qu'à la fin |
| Dépendances incompatibles | Notebook ou conteneur en échec | Utiliser un venv et figer les versions après validation |
| Docker trop volumineux ou manque de mémoire | Construction lente / redémarrages | Utiliser une image slim, tensorflow-cpu et 2 Go de mémoire côté Container Apps comme demandé |
| Permissions Azure insuffisantes | Déploiement bloqué | Utiliser l'utilisateur administrateur du registre ; déploiement manuel prévu par le brief |
| Coût Azure non maîtrisé | Dépenses inutiles | Vérifier le coût estimé, relever le coût réel, supprimer les ressources à la fin sans supprimer un groupe partagé |
| Délais trop courts | Livrables incomplets | Avancer les documents C12 dès J1 ; conserver les preuves au fur et à mesure ; signaler les écarts |

## 6. Suivi des charges et des versions

- Mettre à jour **Charge réelle** dès qu'une tâche est terminée ; conserver les estimations initiales.
- Enregistrer les déploiements dans `PROCEDURE_MISE_EN_PRODUCTION.md` : date, identifiant de commit, modification, résultat.
- Conserver les captures ou sorties de commandes demandées (tests, CI verte/rouge, conteneur, Azure, rollback, suppression).
- À la fin, comparer charge totale prévue (32 h 15), charge réelle et temps disponible (35 h), puis expliquer les écarts dans la fiche finale.

## 7. Fin de projet et responsabilités

L'apprenant décide et exécute les mises en production manuelles et le retour arrière, sous réserve des validations demandées par le formateur. Préparer dès J1 la procédure de mise en production et le plan de fin de vie, puis les compléter avec les commits et les ressources réellement créées. La fin de vie partielle (ancienne version, image obsolète) et totale (application, environnement, registre, secrets et données selon règles du projet) seront distinguées dans `FIN_DE_VIE.md`.
