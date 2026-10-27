# PROCÉDURE DE MISE EN PRODUCTION

**Projet :** Classification de résumés de films (horreur / comédie) — API FastAPI  
**Compétence :** C12 - Planifier le projet  
**Responsable des décisions et de l'exécution :** Apprenant (projet individuel)  
**Environnement cible :** Azure Container Apps, image stockée dans Azure Container Registry (ACR)

## 1. Déclencheur et préparation

Une mise en production est envisagée lorsqu'une modification du modèle, du prétraitement ou de l'API est terminée et validée localement. Avant de publier, je vérifie que le notebook s'exécute, que les fichiers du dossier `model/` sont cohérents (modèle `.keras`, vectoriseur TF-IDF, `metrics.json`) et que les changements sont enregistrés dans Git. Je conserve l'identifiant du commit (`git rev-parse HEAD`) pour assurer la traçabilité.

## 2. Vérifications avant déploiement

1. Lancer les tests automatisés (`pytest`) : route `/health`, prédiction valide, rejet d'une entrée invalide et score minimal du modèle.
2. Exécuter la barrière qualité : comparer le F1 et la taille du test consignés dans `metrics.json` aux seuils de `config.yaml`.
3. Vérifier que GitHub Actions réussit les jobs **test**, **image** et **publier** après le `git push`. Le job de publication doit envoyer dans ACR une image identifiée par le commit.
4. En cas d'échec d'un contrôle, **ne pas déployer** ; corriger, puis relancer les vérifications.

## 3. Déploiement manuel sur Azure

En raison des droits *Contributeur* du compte de formation, la publication de l'image est automatisée, mais son déploiement est manuel.

1. Dans Azure Container Registry, vérifier la présence de l'image correspondant au commit validé.
2. Dans Azure Container Apps, sélectionner cette image et son étiquette de commit ; utiliser l'authentification au registre par **identifiants administrateur stockés comme secrets**, et non par identité managée.
3. Vérifier la configuration de l'application : **1 vCPU, 2 Gio de mémoire**, accès externe activé et port cible correspondant à celui de FastAPI.
4. Déployer la nouvelle version et attendre que l'application démarre correctement.

## 4. Contrôles après déploiement

Tester l'URL publique : `/health` doit répondre `ok` avec la version attendue ; `/docs` doit être accessible ; `/predict` doit produire une classe et une probabilité pour un texte valide, et une erreur claire pour un texte invalide ou trop court. Vérifier les journaux de l'application si nécessaire. Inscrire le résultat et l'identifiant du commit dans le journal ci-dessous.

## 5. Conditions et procédure de retour arrière

**Déclencheurs :** application indisponible, démarrage en échec, erreur de prédiction ou régression importante détectée après déploiement.

1. Identifier dans le journal le **dernier commit fonctionnel** et vérifier que son image existe toujours dans ACR.
2. Dans Azure Container Apps, redéployer manuellement l'image correspondant à cet ancien commit.
3. Contrôler de nouveau `/health` et `/predict` ; vérifier que la version précédente est rétablie (et que `/hello` disparaît si elle avait été ajoutée dans la nouvelle version).
4. Consigner la cause, le commit restauré et le résultat. Ne pas supprimer l'ancienne image avant validation de la nouvelle version.

## 6. Journal des versions déployées

| Date  | Commit déployé | Changement | Résultat / vérifications | Décision ou retour arrière |
|---|---|---|---|---|
| 27/10/2026 | `40515fa` | Première mise en production | API FastAPI déployée sur Azure Container Apps ; routes `/health`, `/docs` et `/predict` testées (captures à joindre) | Version initiale conservée pour permettre un retour arrière |
| 27/10/2026 | `1aa2a70` | Ajout des routes `/hello` et `/stephan` | Nouvelle image publiée dans ACR et version déployée ; vérifier les captures des routes publiques | Nouvelle version destinée à démontrer le changement applicatif |
| 27/10/2026 | `40515fa` | Retour arrière vers l’image précédente | Retour arrière expérimenté ; résultat final des vérifications `/health` et `/predict` à confirmer par capture | Restauration de la version antérieure |

