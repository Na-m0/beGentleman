from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QHBoxLayout, QLineEdit, QPushButton, QCheckBox, QFileDialog
from PyQt6.QtGui import QMovie
from PyQt6.QtCore import Qt, QSize
from ui.message_bubble import MessageBubble
from core.analyse_thread import AnalyseThread
import pytesseract
from PIL import Image

class AnalyseWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #3c3c3c; color: white;")
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 30, 50, 30)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.chat_content = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_content)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_area.setWidget(self.chat_content)
        self.scroll_area.setStyleSheet("border: none;")

        self.chat_layout.addWidget(MessageBubble("Bonjour jeune homme, comment puis-je vous aider aujourd'hui ?", avatar_path="ressources/logo.png"))
        self.chat_layout.addWidget(MessageBubble("J’aurais besoin d’aide pour une fille…..", avatar_path="ressources/avatar.png", is_user=True))

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
        for cb in [self.checkbox_msg, self.checkbox_analyse]:
            cb.setStyleSheet("color: white;")
            checkbox_column.addWidget(cb)

        input_row.addLayout(checkbox_column)

        image_layout = QHBoxLayout()
        self.btn_image = QPushButton("Ajouter une image")
        self.btn_image.setStyleSheet("background: transparent; color: white;")
        self.btn_image.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_image.clicked.connect(self.analyser_image)
        image_layout.addWidget(self.btn_image)
        image_layout.addStretch()

        self.context_input = QLineEdit()
        self.context_input.setPlaceholderText("Décrire votre situation")
        self.context_input.setStyleSheet("""
            background-color: #555;
            border: none;
            border-radius: 10px;
            padding: 10px;
            color: white;
        """)

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

        self.loader = QLabel()
        self.loader.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loader.setVisible(False)
        self.movie = QMovie("ressources/lg.gif")
        self.loader.setMovie(self.movie)

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
        self.loader_gif = QMovie("ressources/lg.gif")
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
                self.chat_layout.addWidget(MessageBubble(section.strip(), avatar_path="ressources/logo.png"))
            elif any(kw in clean for kw in ["analyse", "interprétation", "explication", "ce que cela signifie"]):
                self.chat_layout.addWidget(MessageBubble(f"🔍 {section.strip()}", avatar_path="ressources/logo.png"))
            else:
                self.chat_layout.addWidget(MessageBubble(section.strip(), avatar_path="ressources/logo.png"))

    def afficher_erreur(self, erreur):
        self.chat_layout.removeWidget(self.loader_msg)
        self.loader_msg.setParent(None)
        self.loader_gif.stop()
        self.chat_layout.addWidget(MessageBubble(f"❌ Erreur : {erreur}", is_user=False))