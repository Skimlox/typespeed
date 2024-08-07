import sys
import requests
import time
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import QTimer

class TypeSpeed(QWidget):
    def __init__(self):
        super().__init__()
        self.quote = self.random_quote_api()  # Fetch a random quote
        self.initUI()
        self.timer_started = False
        self.input_disabled = False

    def initUI(self):
        self.layout = QVBoxLayout()

        self.instruction_label = QLabel("Type the quote below:")
        self.layout.addWidget(self.instruction_label)

        self.text_label = QLabel(self.quote)
        self.layout.addWidget(self.text_label)

        self.progress_label = QLabel("Typing speed: 0 WPM | Accuracy: 0%")
        self.layout.addWidget(self.progress_label)

        self.text_input = QLineEdit()
        self.text_input.textChanged.connect(self.onTextChanged)
        self.layout.addWidget(self.text_input)

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.resetTest)
        self.layout.addWidget(self.reset_button)

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateTimer)
        self.timer.setInterval(100)  
        self.start_time = None

        self.setLayout(self.layout)
        self.setWindowTitle('Typing Speed Test')

        
        self.apply_stylesheet('design.qss')

    def apply_stylesheet(self, filename):
        try:
            with open(filename, 'r') as file:
                stylesheet = file.read()
                self.setStyleSheet(stylesheet)
        except FileNotFoundError:
            QMessageBox.warning(self, "Style Error", f"Stylesheet file {filename} not found.")

    def random_quote_api(self):
        try:
            response = requests.get('https://api.quotable.io/random')
            response.raise_for_status()
            data = response.json()
            return data['content']
        except requests.RequestException as e:
            QMessageBox.warning(self, "Quote Error", f"Error fetching quote: {e}\nUsing default quote.")
            return "Type in a message: Hello World"

    def onTextChanged(self):
        if not self.timer_started and self.text_input.text():
            self.startTypingTest()
        
        if self.start_time:
            current_text = self.text_input.text()
            correct_chars = sum(1 for c1, c2 in zip(current_text, self.text_label.text()) if c1 == c2)
            total_chars = len(self.text_label.text())
            accuracy = (correct_chars / total_chars) * 100 if total_chars > 0 else 0

            elapsed_time = time.time() - self.start_time
            words = len(current_text.split())
            wpm = (words / (elapsed_time / 60)) if elapsed_time > 0 else 0

            self.progress_label.setText(f"Typing speed: {wpm:.2f} WPM | Accuracy: {accuracy:.2f}%")

            if current_text == self.text_label.text():
                self.timer.stop()
                self.progress_label.setText(f"Typing speed: {wpm:.2f} WPM | Accuracy: 100% (Complete!)")
                self.text_input.setDisabled(True)  

            if not self.input_disabled:
                if self.text_input.text() != self.text_label.text()[:len(self.text_input.text())]:
                    self.input_disabled = True
                    self.text_input.setDisabled(True)
                    self.progress_label.setText("Typing speed: 0 WPM | Accuracy: 0% (Incorrect character typed!)")

    def startTypingTest(self):
        self.start_time = time.time()
        self.text_input.clear()
        self.text_input.setFocus()
        self.timer.start()
        self.timer_started = True
        self.input_disabled = False

    def resetTest(self):
        self.timer.stop()
        self.text_input.clear()
        self.progress_label.setText("Typing speed: 0 WPM | Accuracy: 0%")
        self.start_time = None
        self.timer_started = False
        self.text_input.setDisabled(False)
        self.quote = self.random_quote_api()  # Fetch a new quote for the next test
        self.text_label.setText(self.quote)  # Update the quote displayed


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = TypeSpeed()
    ex.show()
    sys.exit(app.exec())