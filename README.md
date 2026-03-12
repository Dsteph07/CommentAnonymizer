# Comment Anonymizer

Outil Python permettant d’anonymiser des données dans un fichier CSV.

Le programme peut anonymiser :

- noms de personnes
- emails
- numéros de téléphone
- adresses IP
- URLs

Deux types d’anonymisation sont disponibles :

- `person`
- `free_text`

Ce guide permet d’installer et d’exécuter le projet **sur un PC Windows vierge utilisant PowerShell**.

---


Il est recommandé d’ouvrir **PowerShell en administrateur**.

---

# 1. Installer Python

winget install Python.Python.3.12

python --version
pip --version

#2. Installer git

winget install Git.Git

git --version

# 3. Cloner le projet

git clone <repository-url>
cd comment_anonymizer

# 4. Environement virtuel

python -m venv venv


.\venv\Scripts\Activate.ps1


# 5. Installer dépendances

pip install -r requirements.txt

# 6. Créer dossier data et ajouter le fichier à anonymiser

mkdir data

#data\input.csv

# 7. Créer le fichier de configuration et adaptez le à vos données  

/config.json

exemple:

{
  "input_csv": "data/input.csv",
  "output_csv": "data/output_anonymized.csv",
  "encoding": "utf-8",
  "delimiter": ";",
  "mapping_output": "data/person_mapping.json",
  "columns": {
    "Short description": "free_text",
    "Comments and work notes": "free_text",
    "Close notes": "free_text",
    "Work notes (Internal View)": "free_text"
  }
}




