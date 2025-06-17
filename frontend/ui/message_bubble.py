from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QSizePolicy
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

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
