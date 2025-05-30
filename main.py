# main.py
import sys
from lib.import_files import move_files, delete_files
from PySide6.QtWidgets import ( 
  QApplication, 
  QLabel, 
  QWidget, 
  QVBoxLayout,
  QPushButton
)

camera_folder = "test_data/fake_camera"
drafts_folder = "test_data/drafts"

class MainWindow(QWidget):
  def __init__(self):
    super().__init__()

    self.setWindowTitle("QuikCap")

    self.output_label = QLabel("Click button to import files")
    self.import_button = QPushButton("Import files")
    self.delete_button = QPushButton("Delete files")

    layout = QVBoxLayout()
    layout.addWidget(self.output_label)
    layout.addWidget(self.import_button)
    layout.addWidget(self.delete_button)

    self.setLayout(layout)
    self.resize(300, 100)

    # events
    self.import_button.clicked.connect(self.handle_import_button_click)
    self.delete_button.clicked.connect(self.handle_delete_button_click)

  def handle_import_button_click(self):
    result = move_files(camera_folder, drafts_folder)
    self.output_label.setText(f"Import complete into {result}")

  def handle_delete_button_click(self):
    result = delete_files(camera_folder)
    self.output_label.setText(f"Delete complete on {result}")

if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec())