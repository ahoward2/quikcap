# main.py
import sys
from lib.import_files import move_files
from PySide6.QtWidgets import ( 
  QApplication, 
  QLabel, 
  QWidget, 
  QVBoxLayout,
  QPushButton
)

class MainWindow(QWidget):
  def __init__(self):
    super().__init__()

    self.setWindowTitle("QuikCap")

    self.output_label = QLabel("Click button to import files")
    

    self.button = QPushButton("Import files")

    layout = QVBoxLayout()
    layout.addWidget(self.output_label)
    layout.addWidget(self.button)

    self.setLayout(layout)
    self.resize(300, 100)

    # events
    self.button.clicked.connect(self.handle_button_click)

  def handle_button_click(self):
    result = move_files()
    self.output_label.setText(result)
  

if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec())