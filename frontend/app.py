import streamlit as st
import requests

st.title("Chatbot Analyste IA 💬")

message_recu = st.text_area("Message reçu")
reponse_utilisateur = st.text_area("Ta réponse prévue")

if st.button("Analyser"):
    payload = {
        "message_recu": message_recu,
        "reponse_utilisateur": reponse_utilisateur
    }
    r = requests.post("http://127.0.0.1:8000/analyser", json=payload)
    if r.status_code == 200:
        result = r.json()
        st.write("🧠 Analyse :")
        st.write(result["analyse"])
    else:
        st.error("Erreur dans l'appel à l'API")
