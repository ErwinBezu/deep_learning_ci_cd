
# FIN_DE_VIE.md — Plan de fin de vie du projet

**Projet :** Classification de résumés de films (horreur / comédie) et mise en production sur Azure  
**Compétence :** C12 - Planifier le projet  
**Responsable :** Apprenant (projet individuel)  
**Statut :** Plan prévisionnel — à compléter lors du nettoyage effectif

## 1. Objectif et périmètre

Ce plan décrit **quand**, **comment** et **dans quel ordre** retirer les composants du projet, ce qui doit être conservé et le coût ou risque associé à leur maintien. Il distingue une **fin de vie partielle** (remplacement d'une version) d'une **fin de vie totale** (arrêt du service et suppression des ressources). Ne jamais supprimer un groupe de ressources Azure partagé.

## 2. Inventaire et décisions de fin de vie

| Composant | Quand le retirer ? | Comment / dans quel ordre ? | À conserver | Coût ou risque si maintenu |
|---|---|---|---|---|
| Modèle `.keras`, TF-IDF `.joblib`, `metrics.json` | Lorsqu'une version est remplacée ; archivage à la clôture | Vérifier le nouveau modèle, conserver la version de retour arrière puis archiver les artefacts nécessaires | Version finale, métriques et éventuellement version précédente | Stockage ; confusion entre versions |
| Image Docker locale | Après validation de l'image publiée ou à la clôture | Supprimer les conteneurs arrêtés puis les images inutilisées (`docker ps -a`, `docker rm`, `docker image rm`) | Dockerfile et identifiants des images/commits | Espace disque local |
| Images dans Azure Container Registry (ACR) | Après la période de retour arrière ; toutes à l'arrêt définitif | Vérifier qu'aucune application n'utilise l'image ; supprimer les anciennes images puis le registre lors de l'arrêt total | Tags et SHA des commits déployés | Stockage et facturation du registre tant qu'il existe |
| Azure Container App | À l'arrêt définitif | Relever les preuves, arrêter le service en supprimant l'application via le portail Azure | URL, configuration non secrète, preuves de tests | Consommation et facturation potentielles |
| Environnement Container Apps | Après suppression de toutes les applications qui l'utilisent | Vérifier qu'il n'est pas partagé, puis supprimer l'environnement | Paramètres utiles documentés | Ressources associées et coûts potentiels |
| Secrets GitHub (identifiants ACR) | Après la dernière publication et l'arrêt du registre | Supprimer les secrets du dépôt ; révoquer ou désactiver les identifiants encore valides | Uniquement les noms des secrets, jamais leurs valeurs | Risque d'accès non autorisé |
| Dépôt GitHub | À la clôture, selon la consigne de rendu | Conserver le dépôt pour l'évaluation ; archiver ou supprimer seulement après validation du formateur | Code, notebook, tests, workflow, documentation et historique | Exposition éventuelle de données ou secrets accidentels |
| Données d'entraînement, de test et de production | À la clôture, selon leur origine et les règles applicables | Supprimer les copies temporaires et fichiers non nécessaires ; ne conserver que les données autorisées | Échantillon de référence autorisé et preuves utiles | Espace disque ; conservation inutile de données |

## 3. Fin de vie partielle : remplacement d'une version

1. Vérifier que les tests et la barrière qualité passent et que l'image correspondant au nouveau commit est disponible dans ACR.
2. Noter dans `PROCEDURE_MISE_EN_PRODUCTION.md` le SHA de l'ancienne version, celui de la nouvelle et la date.
3. Déployer **manuellement** la nouvelle image sur Azure Container Apps.
4. Vérifier `/health` et `/predict` sur l'adresse publique, avec les cas de test attendus.
5. En cas d'échec, redéployer manuellement l'image de l'ancien commit et vérifier les routes.
6. Ne retirer l'ancienne image qu'après validation de la nouvelle version et lorsque le retour arrière n'est plus nécessaire.

**Résultat attendu :** service fonctionnel, historique de versions traçable et possibilité de revenir à la version précédente pendant la période de validation.

## 4. Fin de vie totale : ordre de suppression

1. **Documenter l'état final :** relever les derniers commits, résultats des tests, URL publique et captures d'écran ; relever le coût estimé et, si disponible, le coût réel dans Azure Cost Management.
2. **Supprimer l'Azure Container App** dans le portail Azure ; vérifier sa disparition.
3. **Supprimer l'environnement Container Apps**, uniquement s'il est propre au projet et n'héberge aucune autre application.
4. **Supprimer Azure Container Registry**, après vérification qu'aucun autre service ne l'utilise ; confirmer sa disparition.
5. **Supprimer les secrets GitHub** associés au registre et révoquer les identifiants encore actifs.
6. **Nettoyer Docker en local** : conteneurs et images inutilisés ; conserver le Dockerfile dans le dépôt.
7. **Nettoyer les données et artefacts temporaires** ; conserver les livrables autorisés et le dépôt pour l'évaluation.
8. **Contrôler l'absence des ressources créées** et enregistrer les preuves et les coûts observés.

**Précaution :** ne pas supprimer le groupe de ressources Azure s'il est partagé avec d'autres apprenants ou projets.

## 5. Vérification et preuves à renseigner

| Contrôle | Résultat / preuve | Date |
|---|---|---|
| Dernier état et SHA du déploiement consignés | À compléter | À compléter |
| Coût Azure estimé relevé | À compléter | À compléter |
| Coût réel Azure relevé (si disponible) | À compléter | À compléter |
| Container App supprimée | À compléter (capture) | À compléter |
| Environnement Container Apps supprimé | À compléter (capture) | À compléter |
| Registre ACR supprimé | À compléter (capture) | À compléter |
| Secrets GitHub supprimés / identifiants révoqués | À compléter | À compléter |
| Images locales et données temporaires nettoyées | À compléter | À compléter |
| Dépôt et livrables conservés pour l'évaluation | À compléter | À compléter |

## 6. Bilan de fin de projet

- **Fin de vie partielle réalisée :** à compléter (version remplacée, rollback testé, résultat).
- **Fin de vie totale réalisée :** à compléter (date, ressources supprimées, preuves).
- **Coût estimé / coût réel :** à compléter ; ne pas confondre estimation et montant facturé.
- **Écarts avec le plan et améliorations :** à compléter dans la fiche finale C12.

> Ce document décrit un plan. Les suppressions et vérifications ne seront considérées comme effectuées qu'une fois réalisées et justifiées par des preuves.
