# main.py
import sys
from lib.import_files import move_files, delete_files
from PySide6.QtWidgets import ( 
  QApplication, 
  QLabel, 
  QWidget, 
  QVBoxLayout,
  QHBoxLayout,
  QPushButton,
  QFrame
)

camera_folder = "test_data/fake_camera"
drafts_folder = "test_data/drafts"

class MainWindow(QWidget):
  def __init__(self):
    super().__init__()

    self.setWindowTitle("QuikCap")
    
    self.main_layout = QVBoxLayout()

    self.output_label = QLabel("Click button to import files")
    self.import_button = QPushButton("Import files")
    self.delete_button = QPushButton("Delete files")

    self.main_layout.addWidget(self.import_button)
    self.main_layout.addWidget(self.delete_button)
    self.main_layout.addStretch()

    self.footer = QFrame()
    self.footer.setFrameShape(QFrame.Shape.NoFrame)

    self.footer_layout = QHBoxLayout()
    self.footer_layout.setContentsMargins(1, 0, 1, 0)
    self.output_label = QLabel("Ready.")
    self.footer_layout.addWidget(self.output_label)

    self.footer.setLayout(self.footer_layout)
    self.main_layout.addWidget(self.footer)

    self.setLayout(self.main_layout)
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