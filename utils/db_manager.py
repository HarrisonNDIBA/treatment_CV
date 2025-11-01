import pandas as pd

def update_profile_status(csv_path, candidate_name, new_status):
    """Met à jour le statut (Profil) d’un candidat dans le CSV."""
    df = pd.read_csv(csv_path)
    df.loc[df["Nom"] == candidate_name, "Profil"] = new_status
    df.to_csv(csv_path, index=False)
