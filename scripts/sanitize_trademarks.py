"""Script d'anonymisation et de conformité juridique (Trademark Sanitizer).

Nettoie et remplace récursivement toutes les occurrences de marques déposées
dans le code source, les notebooks, les configurations et la documentation.
"""

import json
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

# Support encodage console Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Mapping des remplacements (du plus spécifique au plus général)
REPLACEMENTS = {
    # URLs et domaines
    r"https?://(?:www\.)?portail-auto-maroc\.local/[^\s\"')]+": "https://portail-auto-maroc.local/annonces",
    r"https?://(?:www\.)?portail-auto-maroc\.local": "https://portail-auto-maroc.local",
    r"www\.portail-auto-maroc\.local": "portail-auto-maroc.local",
    # Fichiers et artefacts
    r"MarketData\.csv": "market_data_raw.csv",
    r"market_data\.csv": "market_data.csv",
    r"market_backup\.json": "market_backup.json",
    # Formulations textuelles
    r"données publiques du marché automobile marocain": "données publiques du marché automobile marocain",
    r"annonces du marché automobile marocain": "annonces du marché automobile marocain",
    r"collecte de données du marché automobile": "collecte de données du marché automobile",
}

FILE_RENAMES = {
    "market_data_raw.csv": "market_data_raw.csv",
    "market_data.csv": "market_data.csv",
    "market_backup.json": "market_backup.json",
}

EXTENSIONS_A_TRAITER = {".py", ".md", ".txt", ".json", ".yaml", ".yml", ".toml", ".html", ".css", ".ipynb"}

IGNORED_DIRS = {".git", ".venv", "venv", "__pycache__", ".pytest_cache", ".backup_sanitization"}


def creer_backup(root_dir: Path) -> Path:
    """Crée une sauvegarde horodatée du projet avant toute modification."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = root_dir / f".backup_sanitization_{timestamp}"
    print(f"📦 Création d'une sauvegarde dans : {backup_dir}")

    def ignore_patterns(folder, files):
        return [f for f in files if f in IGNORED_DIRS or f.startswith(".backup_")]

    shutil.copytree(root_dir, backup_dir, ignore=ignore_patterns)
    print("✅ Sauvegarde terminée avec succès.\n")
    return backup_dir


def nettoyer_texte(contenu: str) -> tuple[str, int]:
    """Applique les règles de remplacement par expressions régulières."""
    total_remplacements = 0
    nouveau_contenu = contenu

    for pattern, replacement in REPLACEMENTS.items():
        nouveau_contenu, count = re.subn(pattern, replacement, nouveau_contenu, flags=re.IGNORECASE)
        total_remplacements += count

    return nouveau_contenu, total_remplacements


def nettoyer_notebook(chemin_nb: Path, vider_outputs: bool = True) -> int:
    """Nettoie un notebook Jupyter (.ipynb) de manière sécurisée en parsant son JSON."""
    try:
        with open(chemin_nb, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"⚠️ Erreur lors de la lecture du notebook {chemin_nb}: {e}")
        return 0

    remplacements = 0

    for cell in data.get("cells", []):
        if "source" in cell:
            if isinstance(cell["source"], list):
                nouvelle_source = []
                for ligne in cell["source"]:
                    propre, cnt = nettoyer_texte(ligne)
                    remplacements += cnt
                    nouvelle_source.append(propre)
                cell["source"] = nouvelle_source
            elif isinstance(cell["source"], str):
                cell["source"], cnt = nettoyer_texte(cell["source"])
                remplacements += cnt

        if vider_outputs and "outputs" in cell:
            nb_outputs_str = json.dumps(cell["outputs"])
            if "portail-auto-maroc" in nb_outputs_str.lower():
                remplacements += 1
                cell["outputs"] = []
                cell["execution_count"] = None

    with open(chemin_nb, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return remplacements


def renommer_fichiers(root_dir: Path):
    """Renomme les fichiers contenant des marques déposées."""
    renommes = []
    for root, _dirs, files in os.walk(root_dir):
        if any(ignored in root for ignored in IGNORED_DIRS):
            continue
        for file in files:
            if file in FILE_RENAMES and file != FILE_RENAMES[file]:
                anc_path = Path(root) / file
                nouveau_nom = FILE_RENAMES[file]
                nouv_path = Path(root) / nouveau_nom
                anc_path.rename(nouv_path)
                renommes.append((str(anc_path), str(nouv_path)))
    return renommes


def executer_sanitisation(root_dir: Path, vider_outputs_notebooks: bool = True):
    """Fonction principale de parcours et d'assainissement."""
    print("=" * 65)
    print(" 🛡️  CONFORMITÉ JURIDIQUE - NETTOYAGE DES MARQUES DÉPOSÉES")
    print("=" * 65)

    backup_dir = creer_backup(root_dir)
    rapport_fichiers = {}
    total_global = 0

    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS and not d.startswith(".backup_")]

        for file in files:
            file_path = Path(root) / file
            ext = file_path.suffix.lower()

            if file_path.name == "sanitize_trademarks.py" or ext not in EXTENSIONS_A_TRAITER:
                continue

            if ext == ".ipynb":
                cnt = nettoyer_notebook(file_path, vider_outputs=vider_outputs_notebooks)
                if cnt > 0:
                    rapport_fichiers[str(file_path.relative_to(root_dir))] = cnt
                    total_global += cnt
            else:
                try:
                    with open(file_path, encoding="utf-8", errors="ignore") as f:
                        contenu = f.read()

                    nouveau_contenu, cnt = nettoyer_texte(contenu)
                    if cnt > 0:
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(nouveau_contenu)
                        rapport_fichiers[str(file_path.relative_to(root_dir))] = cnt
                        total_global += cnt
                except OSError as e:
                    print(f"⚠️ Erreur d'accès fichier sur {file_path}: {e}")

    fichiers_renommes = renommer_fichiers(root_dir)

    print("-" * 65)
    print(f"📋 RAPPORT D'ANONYMISATION : {total_global} occurrences remplacées")
    print("-" * 65)
    for fichier, count in sorted(rapport_fichiers.items(), key=lambda x: -x[1]):
        print(f"  • {fichier:<45} : {count:>5} remplacements")

    if fichiers_renommes:
        print("\n📁 FICHIERS PHYSIQUES RENOMMÉS :")
        for anc, nouv in fichiers_renommes:
            print(f"  • {Path(anc).name} ➔ {Path(nouv).name}")

    print("-" * 65)
    print("✅ Nettoyage terminé avec succès.")
    print(f"ℹ️ Sauvegarde : {backup_dir}")
    print("=" * 65)


if __name__ == "__main__":
    racine_projet = Path(__file__).resolve().parent.parent
    executer_sanitisation(racine_projet, vider_outputs_notebooks=True)
