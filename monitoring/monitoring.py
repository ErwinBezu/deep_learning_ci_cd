from pathlib import Path

import pandas as pd
from evidently import DataDefinition, Dataset, Report
from evidently.presets import DataDriftPreset

DOSSIER_MONITORING = Path(__file__).resolve().parent
FICHIER_REFERENCE = DOSSIER_MONITORING / "reference2.csv"
DOSSIER_RAPPORTS = DOSSIER_MONITORING / "rapports"
DOSSIER_RAPPORTS.mkdir(parents=True, exist_ok=True)

reference = pd.read_csv(FICHIER_REFERENCE)
colonnes_requises = {"titre", "resume", "cible"}
if not colonnes_requises.issubset(reference.columns):
    raise ValueError(f"Colonnes attendues : {sorted(colonnes_requises)}")
if reference["resume"].isna().any():
    raise ValueError("Des résumés sont manquants dans les données de référence.")


def caracteristiques(df: pd.DataFrame) -> pd.DataFrame:
    textes = df["resume"].astype(str)
    return pd.DataFrame({
        "longueur_resume": textes.str.len(),
        "nombre_mots": textes.str.split().str.len(),
    })


def generer_rapport(nom: str, donnees_courantes: pd.DataFrame) -> None:
    colonnes = ["longueur_resume", "nombre_mots"]
    definition = DataDefinition(numerical_columns=colonnes)
    jeu_reference = Dataset.from_pandas(caracteristiques(reference), data_definition=definition)
    jeu_courant = Dataset.from_pandas(caracteristiques(donnees_courantes), data_definition=definition)
    rapport = Report([DataDriftPreset()])
    resultat = rapport.run(reference_data=jeu_reference, current_data=jeu_courant)
    chemin = DOSSIER_RAPPORTS / f"{nom}.html"
    resultat.save_html(str(chemin))
    print(f"Rapport {nom} : {chemin}")


print(f"Films de référence : {len(reference)}")
print("Répartition des classes :", reference["cible"].value_counts().to_dict())

# Contrôle : les mêmes données des deux côtés, aucune dérive attendue.
generer_rapport("scenario_normal", reference.copy())

# Simulation : raccourcissement variable pour éviter une longueur constante.
production_drift = reference.copy()
production_drift["resume"] = [
    texte[:35 + (i % 21)]
    for i, texte in enumerate(production_drift["resume"].astype(str))
]
generer_rapport("scenario_derive", production_drift)

print("Terminé. Ouvre les deux rapports HTML dans monitoring/rapports/.")
