import sys
import requests
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QLineEdit, QCheckBox, QScrollArea, QSizePolicy,
    QMainWindow, QFileDialog
)
from PyQt6.QtGui import QPixmap, QMovie
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize
import pytesseract
from PIL import Image



class MessageBubble(QWidget):
    def __init__(self, text, avatar_path=None, is_user=False):
        super().__init__()
        layout = QHBoxLayout()
        bubble = QLabel(text)
        bubble.setWordWrap(True)

        if is_user:
            bubble.setStyleSheet("""
                background-color: #d32f2f;
                color: white;
                padding: 10px;
                border-radius: 10px;
            """)
        else:
            if text.startswith("🔍"):
                bubble.setStyleSheet("""
                    background-color: #005f73;
                    color: white;
                    padding: 10px;
                    border-radius: 10px;
                    font-style: italic;
                """)
            else:
                bubble.setStyleSheet("""
                    background-color: #444;
                    color: white;
                    padding: 10px;
                    border-radius: 10px;
                """)

        bubble.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        avatar = QLabel()
        if avatar_path:
            pixmap = QPixmap(avatar_path).scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            avatar.setPixmap(pixmap)
            avatar.setFixedSize(40, 40)

        if is_user:
            layout.addWidget(bubble)
            layout.addWidget(avatar)
            layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        else:
            layout.addWidget(avatar)
            layout.addWidget(bubble)
            layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.setLayout(layout)


class AccueilWindow(QWidget):
    def __init__(self, switch_callback):
        super().__init__()
        self.switch_callback = switch_callback
        self.setStyleSheet("background-color: black;")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        image = QLabel()
        pixmap = QPixmap("logo.png")
        image.setPixmap(pixmap.scaledToHeight(350, Qt.TransformationMode.SmoothTransformation))
        image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        button = QPushButton("Besoin d’aide ?")
        button.setFixedSize(160, 40)
        button.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                font-weight: bold;
                font-size: 14px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #cc0000;
            }
        """)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(self.switch_callback)

        button_wrapper = QHBoxLayout()
        button_wrapper.addStretch()
        button_wrapper.addWidget(button)
        button_wrapper.addStretch()

        layout.addWidget(image)
        layout.addLayout(button_wrapper)
        self.setLayout(layout)


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


class AnalyseWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #3c3c3c; color: white;")
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 30, 50, 30)

        # Zone de conversation
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.chat_content = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_content)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_area.setWidget(self.chat_content)
        self.scroll_area.setStyleSheet("border: none;")

        self.chat_layout.addWidget(MessageBubble("Bonjour jeune homme, comment puis-je vous aider aujourd'hui ?", avatar_path="logo.png"))
        self.chat_layout.addWidget(MessageBubble("J’aurais besoin d’aide pour une fille…..", avatar_path="avatar.png", is_user=True))

        # Ligne 1 : input message + checkboxes
        input_row = QHBoxLayout()
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Message recu")
        self.message_input.setStyleSheet("""
            background-color: #555;
            border: none;
            border-radius: 10px;
            padding: 10px;
            color: white;
        """)
        input_row.addWidget(self.message_input)

        checkbox_column = QVBoxLayout()
        checkbox_column.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.checkbox_msg = QCheckBox("Faire un message de réponse")
        self.checkbox_analyse = QCheckBox("Analyse complète")
        self.checkbox_graph = QCheckBox("Graphique de compatibilité")
        for cb in [self.checkbox_msg, self.checkbox_analyse, self.checkbox_graph]:
            cb.setStyleSheet("color: white;")
            checkbox_column.addWidget(cb)

        input_row.addLayout(checkbox_column)

        # Ligne 2 : bouton image
        image_layout = QHBoxLayout()
        self.btn_image = QPushButton("Ajouter une image")
        self.btn_image.setStyleSheet("background: transparent; color: white;")
        self.btn_image.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_image.clicked.connect(self.analyser_image)
        image_layout.addWidget(self.btn_image)
        image_layout.addStretch()

        # Ligne 3 : input contexte
        self.context_input = QLineEdit()
        self.context_input.setPlaceholderText("Décrire votre situation")
        self.context_input.setStyleSheet("""
            background-color: #555;
            border: none;
            border-radius: 10px;
            padding: 10px;
            color: white;
        """)

        # Ligne 4 : bouton envoyer
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.btn_add = QPushButton("Envoyer")
        self.btn_add.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                font-weight: bold;
                font-size: 14px;
                padding: 8px 20px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #cc0000;
            }
        """)
        self.btn_add.clicked.connect(self.demarrer_analyse)
        button_layout.addWidget(self.btn_add)

        # Loader gif
        self.loader = QLabel()
        self.loader.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loader.setVisible(False)
        self.movie = QMovie("lg.gif")
        self.loader.setMovie(self.movie)

        # Ajout final au layout
        main_layout.addWidget(self.scroll_area)
        main_layout.addLayout(input_row)
        main_layout.addLayout(image_layout)
        main_layout.addWidget(self.context_input)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.loader)

        self.setLayout(main_layout)

    def demarrer_analyse(self):
        msg = self.message_input.text().strip()
        contexte = self.context_input.text().strip()
        rep = "Réponse fictive"

        if not msg:
            return

        self.chat_layout.addWidget(MessageBubble(msg, avatar_path="avatar.png", is_user=True))
        self.message_input.clear()
        self.context_input.clear()

        self.afficher_loader()

        faire_reponse = self.checkbox_msg.isChecked()
        analyse_complete = self.checkbox_analyse.isChecked()

        self.thread = AnalyseThread(msg, rep, faire_reponse, analyse_complete, contexte)
        self.thread.result_ready.connect(self.afficher_resultat)
        self.thread.error_occurred.connect(self.afficher_erreur)
        self.thread.start()

    def analyser_image(self):
        file, _ = QFileDialog.getOpenFileName(self, "Choisir une image", "", "Images (*.png *.jpg *.jpeg)")
        if file:
            try:
                text = pytesseract.image_to_string(Image.open(file))
                if text.strip():
                    self.chat_layout.addWidget(MessageBubble("[📷 Analyse de la capture envoyée]", avatar_path="avatar.png", is_user=True))
                    self.afficher_loader()
                    self.thread = AnalyseThread(text.strip(), "Réponse fictive", True, True)
                    self.thread.result_ready.connect(self.afficher_resultat)
                    self.thread.error_occurred.connect(self.afficher_erreur)
                    self.thread.start()
                else:
                    self.chat_layout.addWidget(MessageBubble("❌ Aucun texte détecté dans l’image.", is_user=False))
            except Exception as e:
                self.chat_layout.addWidget(MessageBubble(f"❌ Erreur OCR : {e}", is_user=False))

    def afficher_loader(self):
        self.loader_msg = QLabel()
        self.loader_msg.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.loader_gif = QMovie("lg.gif")
        self.loader_gif.setScaledSize(QSize(40, 40))
        self.loader_msg.setMovie(self.loader_gif)
        self.loader_gif.start()
        self.chat_layout.addWidget(self.loader_msg)

    def afficher_resultat(self, texte):
        self.chat_layout.removeWidget(self.loader_msg)
        self.loader_msg.setParent(None)
        self.loader_gif.stop()

        for section in texte.split("\n\n"):
            clean = section.strip().lower()
            if any(kw in clean for kw in ["réponse", "suggestion", "à envoyer"]):
                self.chat_layout.addWidget(MessageBubble(section.strip(), avatar_path="logo.png"))
            elif any(kw in clean for kw in ["analyse", "interprétation", "explication", "ce que cela signifie"]):
                self.chat_layout.addWidget(MessageBubble(f"🔍 {section.strip()}", avatar_path="logo.png"))
            else:
                self.chat_layout.addWidget(MessageBubble(section.strip(), avatar_path="logo.png"))

    def afficher_erreur(self, erreur):
        self.chat_layout.removeWidget(self.loader_msg)
        self.loader_msg.setParent(None)
        self.loader_gif.stop()
        self.chat_layout.addWidget(MessageBubble(f"❌ Erreur : {erreur}", is_user=False))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gentleman")
        self.resize(800, 600)
        self.accueil = AccueilWindow(self.afficher_analyse)
        self.analyse = AnalyseWindow()
        self.setCentralWidget(self.accueil)

    def afficher_analyse(self):
        self.setCentralWidget(self.analyse)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
