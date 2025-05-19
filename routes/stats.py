# routes/stats.py

import os
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

DATA_FILE = "data/responses.csv"

# 🎛️ Filtres dynamiques
st.sidebar.title("🎚️ Filtres")

# Chargement des données
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    st.error("Le fichier de données est introuvable.")
    st.stop()

# Récupération des options disponibles dans les données
classes = df["classe"].dropna().unique().tolist()
sexes = df["sexe"].dropna().unique().tolist()

selected_classes = st.sidebar.multiselect(
    "Filtrer par classe :",
    options=classes,
    default=classes
)
selected_sexes = st.sidebar.multiselect(
    "Filtrer par sexe :",
    options=sexes,
    default=sexes
    )
age_min, age_max = int(df["age"].min()), int(df["age"].max())
selected_age = st.sidebar.slider(
    "Tranche d'âge :",
    min_value=age_min,
    max_value=age_max,
    value=(age_min, age_max)
    )


# Application des filtres
df = df[
    df["classe"].isin(selected_classes) &
    df["sexe"].isin(selected_sexes) &
    df["age"].between(selected_age[0], selected_age[1])
    ]


def display():
    st.title("📊 Statistiques & Analyse enrichie")

    if not os.path.exists(DATA_FILE):
        st.warning("⚠️ Aucune donnée disponible.")
        return

    df = pd.read_csv(DATA_FILE)

    st.subheader("📌 Données Générales")
    st.write(f"**Nombre total de réponses** : {len(df)}")
    st.dataframe(df.tail(5), use_container_width=True)

    # -------------------------
    # 🥧 Camemberts
    # -------------------------
    st.subheader("🥧 Répartition par sexe")
    fig1, ax1 = plt.subplots()
    df["sexe"].value_counts().plot(
        kind="pie", autopct="%1.1f%%", startangle=90, ax=ax1
    )
    ax1.axis("equal")
    st.pyplot(fig1)

    st.subheader("🥧 Répartition par classe")
    fig2, ax2 = plt.subplots()
    df["classe"].value_counts().plot(
        kind="pie", autopct="%1.1f%%", startangle=90, ax=ax2
    )
    ax2.axis("equal")
    st.pyplot(fig2)

    # -------------------------
    # 📊 Segmentation croisée
    # -------------------------
    st.subheader("📌 Stress moyen par classe")
    stress_map = {
        "Très faible": 1,
        "Faible": 2,
        "Moyen": 3,
        "Élevé": 4,
        "Très élevé": 5,
    }
    if "niveau_stress" in df and "classe" in df:
        df["stress_score"] = df["niveau_stress"].map(stress_map)
        stress_by_class = (
            df.groupby("classe")["stress_score"]
            .mean()
            .sort_values()
            )
        st.bar_chart(stress_by_class)

    st.subheader("📌 Fréquence de tristesse selon le sexe")
    if "tristesse" in df and "sexe" in df:
        triste_crosstab = pd.crosstab(df["sexe"], df["tristesse"])
        st.dataframe(triste_crosstab)

    # -------------------------
    # 📈 Corrélations
    # -------------------------
    st.subheader("📉 Corrélations entre facteurs (codés)")
    correlation_fields = {
        "soutien_famille": {
            "Non, pas du tout": 1,
            "Plutôt non": 2,
            "Plutôt oui": 3,
            "Oui, tout à fait": 4,
        },
        "solitude": {
            "Jamais": 1,
            "Rarement": 2,
            "Parfois": 3,
            "Souvent": 4,
            "Très souvent": 5,
        },
        "sommeil": {
            "Moins de 6h": 1,
            "6 à 7h": 2,
            "7 à 8h": 3,
            "Plus de 8h": 4
            },
        "niveau_stress": stress_map,
    }

    for col, mapping in correlation_fields.items():
        if col in df:
            df[f"{col}_num"] = df[col].map(mapping)

    corr_cols = [col for col in df.columns if col.endswith("_num")]
    if len(corr_cols) > 1:
        corr_matrix = df[corr_cols].corr()
        st.write("📌 Matrice de corrélation (valeurs numériques) :")
        st.dataframe(corr_matrix.round(2))

        st.subheader("🧠 Carte de chaleur des corrélations")
        fig_corr, ax_corr = plt.subplots()
        sns.heatmap(
            corr_matrix,
            annot=True, cmap="coolwarm",
            center=0, ax=ax_corr
            )
        st.pyplot(fig_corr)

    # -------------------------
    # 💬 Extraits de commentaires
    # -------------------------
    st.subheader("🗣️ Commentaires libres")
    comments = df["commentaire_libre"].dropna()
    for i, c in enumerate(comments.sample(min(3, len(comments)))):
        st.markdown(f"> *{c.strip()}*")
