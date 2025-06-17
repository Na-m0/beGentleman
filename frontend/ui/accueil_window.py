from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

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
        pixmap = QPixmap("ressources/logo.png")
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
