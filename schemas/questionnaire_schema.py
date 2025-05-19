import streamlit as st
import unicodedata
import re


def clean_key(label: str) -> str:
    """
    Nettoie un label pour générer une clé Python valide et cohérente.
    Exemple : "Un membre de l’établissement" → "un_membre_de_l_etablissement"
    """
    label = (
        unicodedata.normalize("NFD", label)
        .encode("ascii", "ignore")
        .decode("utf-8")
    )  # Supprimer accents
    label = label.lower()
    label = label.replace("l'etablissement", "l_etablissement")
    label = label.replace("letablissement", "l_etablissement")
    label = re.sub(r"[^\w\s]", "", label)
    label = re.sub(r"\s+", "_", label)
    return label


def general_info_section():
    data = {}
    data["age"] = st.number_input(
        "Âge", min_value=10, max_value=25, step=1, format="%d"
    )
    data["sexe"] = st.radio(
        "Sexe", ["Féminin", "Masculin", "Autre", "Je préfère ne pas dire"]
    )
    data["classe"] = st.selectbox(
        "Classe", ["Seconde", "Première", "Terminale", "Autre"]
    )
    return data


def harassment_experience_section():
    data = {}
    options = [
        "Moqueries",
        "Insultes",
        "Menaces",
        "Coups",
        "Exclusion de groupe",
        "Cyberviolence",
        "Rien",
    ]
    data["harcelement_victime"] = st.multiselect(
        "Tu as été la cible de :", options
    )
    data["harcelement_temoin"] = st.multiselect(
        "Tu as été témoin de :",
        options
        )
    data["harcelement_auteur"] = st.multiselect(
        "Tu as été l’auteur de :",
        options
    )
    return data


def awareness_section():
    data = {}
    sensibilisation_options = [
        "Intervenants extérieurs (asso / police / autres)",
        "Personnel de l’établissement",
        "Personne",
    ]
    data["sensibilisation"] = st.radio(
        "Depuis la 6e, tu as été sensibilisé au harcèlement par :",
        sensibilisation_options,
    )
    return data


def witness_response_section():
    data = {}
    acteurs = [
        "Un Prof",
        "Le Prof Principal",
        "Le Référent Vie Scolaire",
        "Un membre de la Vie Scolaire",
        "Un membre de la direction",
        "Un membre de l’établissement",
        "Un membre de ma famille",
        "Une tierce personne",
        "Le 3018",
    ]
    for personne in acteurs:
        key_name = f"signalement_{clean_key(personne)}"
        print(f"Clé générée : {key_name}")  # Debug
        data[key_name] = st.radio(
            f"Préviendrais-tu {personne} ?", ["Oui", "Non"], key=key_name
        )
    return data


def digital_life_section():
    data = {}
    data["possede_smartphone"] = st.text_input(
        "Depuis quand possèdes-tu un téléphone / smartphone ?"
    )
    plateformes = ["X", "Facebook", "Instagram", "TikTok", "Snap", "Autre"]
    data["comptes_possedes"] = st.multiselect(
        "Tu possèdes un compte sur :", plateformes
    )
    exposition = [
        "Contenus violents",
        "Contenus pornographiques",
        "Jamais été confronté",
    ]
    data["contenus_exposes"] = st.multiselect(
        "Tu as déjà été confronté à :", exposition
    )
    data["contenus_choquants"] = st.multiselect(
        "Tu t’es déjà senti choqué par :", exposition
    )
    return data


def mental_health_section():
    data = {}
    frequences = [
        "Jamais",
        "Plusieurs jours",
        "Plus de la moitié des jours",
        "Presque tous les jours",
    ]
    data["tristesse"] = st.radio(
        (
            "Au cours des 2 dernières semaines, à quelle fréquence t'es-tu "
            "senti triste ou désespéré ?"
        ),
        frequences,
    )
    data["plaisir"] = st.radio(
        (
            "À quelle fréquence as-tu eu peu d’intérêt ou de plaisir "
            "à faire les choses ?"
        ),
        frequences,
    )
    stress_niveau = ["Très faible", "Faible", "Moyen", "Élevé", "Très élevé"]
    data["niveau_stress"] = st.radio(
        "Ton niveau de stress général est :", stress_niveau
    )
    vision_avenir = [
        "Oui, tout à fait",
        "Plutôt oui",
        "Plutôt non",
        "Non, pas du tout"
        ]
    data["vision_avenir"] = st.radio(
        "As-tu une vision positive de l’avenir ?", vision_avenir
    )
    return data


def social_relations_section():
    data = {}
    data["soutien_amis"] = st.radio(
        "Te sens-tu soutenu(e) par tes amis ?",
        ["Oui, tout à fait", "Plutôt oui", "Plutôt non", "Non, pas du tout"],
    )
    data["soutien_famille"] = st.radio(
        "Te sens-tu soutenu(e) par ta famille ?",
        ["Oui, tout à fait", "Plutôt oui", "Plutôt non", "Non, pas du tout"],
    )
    data["solitude"] = st.radio(
        "Te sens-tu souvent seul(e) ?",
        ["Jamais", "Rarement", "Parfois", "Souvent", "Très souvent"],
    )
    data["a_confier"] = st.radio(
        "As-tu des personnes à qui te confier ?",
        ["Oui, tout à fait", "Plutôt oui", "Plutôt non", "Non, pas du tout"],
    )
    return data


def school_life_section():
    data = {}
    freqs = ["Jamais", "Rarement", "Parfois", "Souvent", "Très souvent"]
    data["stress_etudes"] = st.radio(
        "Te sens-tu stressé(e) par tes études ?",
        freqs
    )
    data["concentration"] = st.radio(
        "As-tu des difficultés à te concentrer ?",
        freqs
        )
    data["securite_ecole"] = st.radio(
        "Te sens-tu en sécurité à l’école ?",
        ["Oui, tout à fait", "Plutôt oui", "Plutôt non", "Non, pas du tout"],
    )
    data["victime_harcelement"] = st.radio(
        "As-tu déjà été victime de harcèlement scolaire ?",
        ["Oui", "Non", "Je préfère ne pas répondre"],
    )
    return data


def physical_wellbeing_section():
    data = {}
    data["sommeil"] = st.radio(
        "Combien d’heures dors-tu en moyenne par nuit ?",
        ["Moins de 6h", "6 à 7h", "7 à 8h", "Plus de 8h"],
    )
    data["activite_physique"] = st.radio(
        "Fais-tu de l’activité physique régulièrement ?", ["Oui", "Non"]
    )
    data["alimentation"] = st.radio(
        "Comment évalues-tu ton alimentation ?",
        [
            "Très saine",
            "Plutôt saine",
            "Moyenne",
            "Plutôt mauvaise",
            "Très mauvaise"],
    )
    return data


def help_section():
    data = {}
    data["parler_pro"] = st.radio(
        "As-tu déjà envisagé de parler à un professionnel ?",
        ["Oui", "Non", "Je ne sais pas"],
    )
    data["vers_qui"] = st.radio(
        "Sais-tu vers qui te tourner dans l’établissement ?", ["Oui", "Non"]
    )
    return data


def open_feedback_section():
    data = {}
    data["commentaire_libre"] = st.text_area(
        "Souhaites-tu partager autre chose ?",
        placeholder="Écris librement ici (facultatif)...",
    )
    return data
