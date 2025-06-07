# main.py
import sys
from lib.transfer_worker import FileTransferWorker
from PySide6.QtCore import QThread
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QFileDialog,
    QTextEdit,
    QMessageBox
)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.thread = None
        self.worker = None

        self.setWindowTitle("QuikCap")
        self.main_layout = QVBoxLayout()

        self.camera_label = QLabel("Camera Path:")
        self.camera_input = QLineEdit()
        self.camera_browse_btn = QPushButton("Browse...")
        self.camera_input.setReadOnly(True)

        self.target_label = QLabel("Target Folder (Dump Directory):")
        self.target_input = QLineEdit()
        self.target_input.setReadOnly(True)
        self.target_browse_btn = QPushButton("Browse...")
        self.import_button = QPushButton("Import files")
        self.delete_button = QPushButton("Delete files")

        self.log_output = QTextEdit("Ready.\n")
        self.log_output.setReadOnly(True)

        self.main_layout.addWidget(self.camera_label)
        self.main_layout.addWidget(self.camera_input)
        self.main_layout.addWidget(self.camera_browse_btn)
        self.main_layout.addWidget(self.target_label)
        self.main_layout.addWidget(self.target_input)
        self.main_layout.addWidget(self.target_browse_btn)
        self.main_layout.addWidget(self.import_button)
        self.main_layout.addWidget(self.delete_button)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.log_output)

        self.setLayout(self.main_layout)
        self.resize(300, 100)

        # events
        self.camera_browse_btn.clicked.connect(self.browse_camera)
        self.target_browse_btn.clicked.connect(self.browse_target)
        self.import_button.clicked.connect(self.do_transfer)
        # self.delete_button.clicked.connect(self.handle_delete_button_click)

    def browse_camera(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Camera Folder")
        if folder:
            self.camera_input.setText(folder)

    def browse_target(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Target Folder")
        if folder:
            self.target_input.setText(folder)

    def do_transfer(self):
        # Ignore if already running
        if self.thread and self.thread.isRunning():
            self.log_output.append("Transfer already in progress.")
            return

        camera_path = self.camera_input.text().strip()
        drafts_folder = self.target_input.text().strip()

        if not drafts_folder:
            QMessageBox.warning(
                self, "Warning", "Please select a target folder.")
            return

        self.import_button.setEnabled(False)
        self.log_output.append("Starting transfer...")

        self.thread = QThread()
        self.worker = FileTransferWorker(camera_path, drafts_folder)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_transfer_complete)
        self.worker.error.connect(self.on_transfer_error)
        self.worker.log.connect(self.log_output.append)
        # Clean up
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.finished.connect(self.on_thread_finished)

        self.thread.start()

    def on_transfer_complete(self, folder):
        QMessageBox.information(self, "Success", f"Files moved to:\n{folder}")

    def on_transfer_error(self, error_msg):
        QMessageBox.critical(self, "Transfer Error", error_msg)

    def on_thread_finished(self):
        self.import_button.setEnabled(True)
        self.thread = None
        self.worker = None

    def closeEvent(self, event):
        if self.thread and self.thread.isRunning():
            self.log_output.append(
                "Waiting for transfer to finish before closing...")
            self.thread.quit()
            self.thread.wait()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
