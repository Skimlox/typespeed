import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window title
        self.setWindowTitle("My PyQt6 App")

        # Set the size of the window
        self.resize(400, 300)

        # Create a label widget
        label = QLabel("Hello, PyQt6!", self)
        label.setGeometry(50, 50, 200, 50)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())