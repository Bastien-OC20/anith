# models/response_model.py

from dataclasses import dataclass, asdict, field
from typing import List, Optional


@dataclass
class QuestionnaireResponse:
    # Metadata
    timestamp: str

    # Informations générales
    age: int
    sexe: str
    classe: str

    # Expériences
    harcelement_victime: List[str]
    harcelement_temoin: List[str]
    harcelement_auteur: List[str]

    # Sensibilisation
    sensibilisation: str

    # Signalements (réactions)
    signalement_Un_Prof: str
    signalement_Le_Prof_Principal: str
    signalement_Le_Référent_Vie_Scolaire: str
    signalement_Un_membre_de_la_Vie_Scolaire: str
    signalement_Un_membre_de_la_direction: str
    signalement_Un_membre_de_l_etablissement: str
    signalement_Un_membre_de_ma_famille: str
    signalement_Une_tierce_personne: str
    signalement_Le_3018: str

    # Vie numérique
    possede_smartphone: str
    comptes_possedes: List[str]
    contenus_exposes: List[str]
    contenus_choquants: List[str]

    # Santé mentale
    tristesse: str
    plaisir: str
    niveau_stress: str
    vision_avenir: str

    # Relations sociales
    soutien_amis: str
    soutien_famille: str
    solitude: str
    a_confier: str

    # Vie scolaire
    stress_etudes: str
    concentration: str
    securite_ecole: str
    victime_harcelement: str

    # Bien-être physique
    sommeil: str
    activite_physique: str
    alimentation: str

    # Recherche d'aide
    parler_pro: str
    vers_qui: str

    # Commentaire libre
    commentaire_libre: Optional[str] = field(default="")

    def to_dict(self) -> dict:
        """
        Convertit l'objet dataclass"
        "en dictionnaire pret a l'enregistrement CSV.
        Les listes sont converties en chaines separees par des virgules.
        """
        result = asdict(self)
        for key, value in result.items():
            if isinstance(value, list):
                result[key] = ", ".join(value)
        return result
