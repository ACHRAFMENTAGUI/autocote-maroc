#!/usr/bin/env python3
"""
Script d'anonymisation et de conformité juridique (Trademark Sanitizer).
Nettoie et remplace récursivement toutes les occurrences de marques déposées ("Marché Auto Maroc")
dans le code source, les notebooks, les configurations et la documentation.
"""

import os
import re
import sys
import json
import shutil
from datetime import datetime
from pathlib import Path

# Support encodage console Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Mapping des remplacements (du plus spécifique au plus général)
REPLACEMENTS = {
    # URLs et domaines
    r"https?://(?:www\.)?Marché Auto Maroc\.ma/[^\s\"')]+": "https://portail-auto-maroc.local/annonces",
    r"https?://(?:www\.)?Marché Auto Maroc\.ma": "https://portail-auto-maroc.local",
    r"www\.Marché Auto Maroc\.ma": "portail-auto-maroc.local",
    r"Marché Auto Maroc\.ma": "marche-auto-maroc",

    # Fichiers et artefacts
    r"MarketData\.csv": "market_data_raw.csv",
    r"market_data\.csv": "market_data.csv",
    r"market_backup\.json": "market_backup.json",
    r"MarketData": "MarketData",
    r"market_data": "market_data",
    r"market_backup": "market_backup",

    # Formulations textuelles fréquentes
    r"données publiques du marché marocain\.ma": "données publiques du marché automobile marocain",
    r"données publiques du marché marocain": "données publiques du marché marocain",
    r"données du marché automobile": "données du marché automobile",
    r"annonces Marché Auto Maroc\.ma": "annonces du marché automobile marocain",
    r"annonces d'Marché Auto Maroc\.ma": "annonces du marché automobile marocain",
    r"annonces réelles d'Marché Auto Maroc\.ma": "annonces réelles du marché marocain",
    r"annonces réelles au Maroc \(Marché Auto Maroc\)": "annonces réelles du marché automobile au Maroc",
    r"scrapées? sur Marché Auto Maroc(?:\.ma)?": "collectées sur des portails publics d'annonces",
    r"collecte de données du marché automobile": "collecte de données du marché automobile",
    r"collecte de données du marché automobile": "Collecte de données du marché automobile",

    # Terme générique (respect de la casse)
    r"Marché Auto Maroc": "Marché Auto Maroc",
    r"Marché Auto Maroc": "marche_auto",
}

# Renommage des fichiers et dossiers physiques
FILE_RENAMES = {
    "market_data_raw.csv": "market_data_raw.csv",
    "market_data.csv": "market_data.csv",
    "market_backup.json": "market_backup.json",
}

EXTENSIONS_A_TRAITER = {
    ".py", ".md", ".txt", ".json", ".yaml", ".yml", ".toml", ".html", ".css", ".ipynb"
}

IGNORED_DIRS = {".git", ".venv", "venv", "__pycache__", ".pytest_cache", ".backup_sanitization"}


def creer_backup(root_dir: Path) -> Path:
    """Crée une copie de sauvegarde horodatée du projet avant toute modification."""
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
        with open(chemin_nb, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"⚠️ Erreur lors de la lecture du notebook {chemin_nb}: {e}")
        return 0

    remplacements = 0

    # Nettoyage cellule par cellule
    for cell in data.get("cells", []):
        # 1. Nettoyer le code source et le markdown
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

        # 2. Vider ou nettoyer les sorties d'exécution (outputs contenant des URLs scrapées)
        if vider_outputs and "outputs" in cell:
            # Si la cellule contient des outputs avec 'Marché Auto Maroc', on les purge pour alléger le repo
            nb_outputs_str = json.dumps(cell["outputs"])
            if "Marché Auto Maroc" in nb_outputs_str.lower():
                remplacements += nb_outputs_str.lower().count("Marché Auto Maroc")
                cell["outputs"] = []
                cell["execution_count"] = None

    with open(chemin_nb, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return remplacements


def renommer_fichiers(root_dir: Path):
    """Renomme les fichiers contenant des marques déposées."""
    renommes = []
    for root, dirs, files in os.walk(root_dir):
        if any(ignored in root for ignored in IGNORED_DIRS):
            continue
        for file in files:
            if file in FILE_RENAMES:
                anc_path = Path(root) / file
                nouveau_nom = FILE_RENAMES[file]
                nouv_path = Path(root) / nouveau_nom
                anc_path.rename(nouv_path)
                renommes.append((str(anc_path), str(nouv_path)))
    return renommes


def executer_sanitisation(root_dir: Path, vider_outputs_notebooks: bool = True):
    """Fonction principale de parcours et d'assainissement."""
    print("=" * 65)
    print(" 🛡️  AUTODÉTECTION & CONFORMITÉ JURIDIQUE - AUTODÉTECTION TRADEMARK")
    print("=" * 65)

    backup_dir = creer_backup(root_dir)

    rapport_fichiers = {}
    total_global = 0

    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS and not d.startswith(".backup_")]
        
        for file in files:
            file_path = Path(root) / file
            ext = file_path.suffix.lower()

            if ext not in EXTENSIONS_A_TRAITER:
                continue

            if ext == ".ipynb":
                cnt = nettoyer_notebook(file_path, vider_outputs=vider_outputs_notebooks)
                if cnt > 0:
                    rapport_fichiers[str(file_path.relative_to(root_dir))] = cnt
                    total_global += cnt
            else:
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        contenu = f.read()

                    nouveau_contenu, cnt = nettoyer_texte(contenu)
                    if cnt > 0:
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(nouveau_contenu)
                        rapport_fichiers[str(file_path.relative_to(root_dir))] = cnt
                        total_global += cnt
                except Exception as e:
                    print(f"⚠️ Erreur sur {file_path}: {e}")

    # Renommage des fichiers physiques
    fichiers_renommes = renommer_fichiers(root_dir)

    # Affichage du rapport
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
    print(f"ℹ️ En cas de besoin, la sauvegarde complète se trouve dans : {backup_dir}")
    print("=" * 65)


if __name__ == "__main__":
    racine_projet = Path(__file__).resolve().parent.parent
    executer_sanitisation(racine_projet, vider_outputs_notebooks=True)
