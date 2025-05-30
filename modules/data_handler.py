# modules/data_handler.py

import os
import csv
from models.response_model import QuestionnaireResponse

DATA_FILE = "data/responses.csv"


def save_response(response: QuestionnaireResponse):
    """
    Sauvegarde une instance de QuestionnaireResponse dans un fichier CSV.
    """
    data_dict = response.to_dict()
    file_exists = os.path.isfile(DATA_FILE)

    try:
        with open(DATA_FILE, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=data_dict.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(data_dict)
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des données : {e}")
