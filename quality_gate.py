import argparse
import json
import sys
from pathlib import Path

import yaml

RACINE = Path(__file__).resolve().parent


def verifier_qualite(metrics_path: Path, config_path: Path) -> bool:
    with config_path.open(encoding="utf-8") as fichier:
        config = yaml.safe_load(fichier)

    with metrics_path.open(encoding="utf-8") as fichier:
        metrics = json.load(fichier)

    f1 = float(metrics["metriques"]["f1_test_final"])
    taille_test = int(metrics["donnees"]["test"])
    f1_min = float(config["qualite"]["f1_minimum"])
    taille_min = int(config["qualite"]["taille_test_minimale"])

    print(f"F1 du modèle       : {f1:.4f} (minimum : {f1_min:.4f})")
    print(f"Taille du test     : {taille_test} (minimum : {taille_min})")

    erreurs = []
    if f1 < f1_min:
        erreurs.append(f"F1 insuffisant : {f1:.4f} < {f1_min:.4f}")
    if taille_test < taille_min:
        erreurs.append(f"Jeu de test trop petit : {taille_test} < {taille_min}")

    if erreurs:
        for erreur in erreurs:
            print(f"ECHEC : {erreur}")
        return False

    print("SUCCES : le modèle respecte les critères de qualité.")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Vérifie les seuils qualité du modèle")
    parser.add_argument(
        "--metrics",
        type=Path,
        default=RACINE / "model" / "metrics.json",
        help="Chemin du fichier de métriques à contrôler",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=RACINE / "config.yaml",
        help="Chemin du fichier de configuration",
    )
    args = parser.parse_args()

    try:
        return 0 if verifier_qualite(args.metrics, args.config) else 1
    except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError) as erreur:
        print(f"ECHEC : impossible de vérifier les métriques : {erreur}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
