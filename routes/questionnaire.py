# routes/questionnaire.py

import streamlit as st
from datetime import datetime
from modules.data_handler import save_response
from schemas.questionnaire_schema import (
    general_info_section,
    harassment_experience_section,
    awareness_section,
    witness_response_section,
    digital_life_section,
    mental_health_section,
    social_relations_section,
    school_life_section,
    physical_wellbeing_section,
    help_section,
    open_feedback_section,
)


def display():
    st.title("📝 Questionnaire sur le Harcèlement et la Santé Mentale")
    st.markdown(
        "Merci de remplir ce questionnaire **anonyme**."
        " Toutes les données seront utilisées uniquement"
        " à des fins d'analyse éducative."
    )

    with st.form("questionnaire_form"):
        responses = {}

        # Chargement de chaque section
        st.subheader("🔍 Informations générales")
        responses.update(general_info_section())

        st.subheader("🚨 Expériences de harcèlement")
        responses.update(harassment_experience_section())

        st.subheader("📢 Sensibilisation au harcèlement")
        responses.update(awareness_section())

        st.subheader("👁️ Réactions en tant que témoin")
        responses.update(witness_response_section())

        st.subheader("📱 Vie numérique")
        responses.update(digital_life_section())

        st.subheader("🧠 Santé mentale et bien-être")
        responses.update(mental_health_section())

        st.subheader("🤝 Relations sociales")
        responses.update(social_relations_section())

        st.subheader("🏫 Vie scolaire")
        responses.update(school_life_section())

        st.subheader("💪 Bien-être physique")
        responses.update(physical_wellbeing_section())

        st.subheader("🆘 Recherche d’aide")
        responses.update(help_section())

        st.subheader("🗣️ Commentaires libres")
        responses.update(open_feedback_section())

        # Soumission
        submitted = st.form_submit_button("📤 Envoyer mes réponses")

        if submitted:
            responses["timestamp"] = datetime.now().isoformat()
            print(responses)  # Debug : Affiche les réponses collectées
            st.write(
                "✅ Champs reçus depuis le formulaire :"
            )
            st.write(
                list(responses.keys())
            )

            from models.response_model import QuestionnaireResponse
            expected_keys = QuestionnaireResponse.__annotations__.keys()
            st.write(
                "✅ Champs attendus par le modèle :",
                list(expected_keys)
            )

            # Filtrer les réponses pour ne garder que les clés attendues
            filtered_responses = {
                k: v for k, v in responses.items() if k in expected_keys
            }

            # Affiche les différences
            unexpected = [
                k for k in responses.keys() if k not in expected_keys
            ]
            if unexpected:
                st.error(f"❌ Clés inconnues dans les réponses : {unexpected}")

            # Créer l'objet QuestionnaireResponse avec les réponses filtrées
            try:
                data = QuestionnaireResponse(**filtered_responses)
                save_response(data)
                st.success("✅ Merci ! Votre réponse a bien été enregistrée.")
            except TypeError as e:
                st.error(
                    f"Erreur lors de la création de l'objet "
                    f"QuestionnaireResponse : {e}"
                )
