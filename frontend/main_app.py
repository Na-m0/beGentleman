import sys
from PyQt6.QtWidgets import QApplication
from ui.accueil_window import AccueilWindow
from ui.analyse_window import AnalyseWindow
from PyQt6.QtWidgets import QMainWindow

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
