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

    with open(DATA_FILE, mode="a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data_dict.keys())

        # Écrire l’en-tête uniquement si le fichier n’existe pas
        if not file_exists:
            writer.writeheader()

        writer.writerow(data_dict)
    print(f"Réponse sauvegardée : {data_dict}")
    print(f"Réponse sauvegardée : {response}")
