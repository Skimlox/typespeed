import requests
from PyQt6.QtWidgets import QMessageBox
def random_quote_api(self):
        try:
            response = requests.get('https://api.quotable.io/random')
            response.raise_for_status()
            data = response.json()
            return data['content']
        except requests.RequestException as e:
            QMessageBox.warning(self, "Error", f"Error fetching quote: {e}\nUsing another quote")
            return "Type in a message: Hello World"