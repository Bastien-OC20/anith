# app.py
import streamlit as st


st.set_page_config(
    page_title="Questionnaire HmS",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded",
)


from routes import questionnaire, stats  # noqa: E402


def main():
    st.sidebar.title("📋 Navigation")
    page = st.sidebar.radio(
        "Aller à :", ("📝 Remplir le questionnaire", "📊 Statistiques")
    )

    if page == "📝 Remplir le questionnaire":
        questionnaire.display()
    elif page == "📊 Statistiques":
        stats.display()

    st.sidebar.markdown("---")
    st.sidebar.info(
        (
            "Application dédiée à la compréhension du bien-être "
            "et du harcèlement scolaire chez les lycéens."
        )
    )


if __name__ == "__main__":
    main()
