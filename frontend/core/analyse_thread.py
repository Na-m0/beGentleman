import requests
from PyQt6.QtCore import QThread, pyqtSignal

class AnalyseThread(QThread):
    result_ready = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self, msg, rep, faire_reponse=False, analyse_complete=False, contexte=""):
        super().__init__()
        self.msg = msg
        self.rep = rep
        self.faire_reponse = faire_reponse
        self.analyse_complete = analyse_complete
        self.contexte = contexte

    def run(self):
        try:
            prompt_extras = ""
            if self.analyse_complete:
                prompt_extras += "\n\nTu dois absolument faire une analyse complète du message de la fille."
            if self.faire_reponse:
                prompt_extras += "\n\nEt propose une réponse gentleman à envoyer."
            if self.contexte.strip():
                prompt_extras += f"\n\nContexte supplémentaire : {self.contexte.strip()}"

            full_text = f"Message reçu : {self.msg}\nRéponse proposée : {self.rep}{prompt_extras}"

            r = requests.post("http://127.0.0.1:8000/analyser", json={
                "message_recu": self.msg,
                "reponse_utilisateur": full_text
            })

            if r.status_code == 200:
                analyse = r.json().get("analyse", {})
                texte = analyse.get("content", str(analyse)) if isinstance(analyse, dict) else str(analyse)
                self.result_ready.emit(texte)
            else:
                self.error_occurred.emit(f"Erreur {r.status_code}")
        except Exception as e:
            self.error_occurred.emit(str(e))
