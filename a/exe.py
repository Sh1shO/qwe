from PySide6.QtWidgets import QApplication
from t1 import MainWindow

app = QApplication([])
window = MainWindow()
window.show()
app.exec()