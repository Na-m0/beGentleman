import streamlit as st
import requests

if "page" not in st.session_state:
    st.session_state.page = "accueil"

if st.session_state.page == "accueil":
    st.image("./logo.png", width=200)
    st.title("Gentleman")
    st.write("Bienvenue sur l'IA Gentleman qui t'aidera à améliorer ta séduction.")
    if st.button("Commencer ➡️"):
        st.session_state.page = "analyse"

elif st.session_state.page == "analyse":
    st.title("Analyse ton message")
    message_recu = st.text_area("Message reçu de la demoiselle")
    reponse_utilisateur = st.text_area("Ta réponse")
    if st.button("Analyser"):
        payload = {
            "message_recu": message_recu,
            "reponse_utilisateur": reponse_utilisateur
        }
        r = requests.post("http://127.0.0.1:8000/analyser", json=payload)
        if r.status_code == 200:
            result = r.json()
            analyse_ia = result["analyse"]

            if isinstance(analyse_ia, dict) and "content" in analyse_ia:
                texte_analyse = analyse_ia["content"]
            else:
                texte_analyse = str(analyse_ia)

            st.markdown("### Analyse... :")
            sections = texte_analyse.split("\n\n")

            for section in sections:
                if section.strip().lower().startswith("réponse optimisée"):
                    st.success(f"💡 **{section}**")
                elif section.strip().lower().startswith("explication"):
                    st.info(f"📌 {section}")
                else:
                    st.markdown(section)



