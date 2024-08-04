import sys
import requests
import time
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import QTimer


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = TypeSpeed()
    ex.show()
    sys.exit(app.exec())