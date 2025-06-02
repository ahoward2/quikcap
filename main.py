# main.py
import sys
from lib.copy_mtp import move_files_from_mtp
from lib.find_devices import get_connected_devices
from lib.transfer_worker import FileTransferWorker
from PySide6.QtCore import QThread
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QComboBox,
    QFileDialog,
    QTextEdit,
    QMessageBox
)

camera_folder = "test_data/fake_camera"
drafts_folder = "test_data/drafts"


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.thread = None
        self.worker = None

        self.setWindowTitle("QuikCap")
        self.main_layout = QVBoxLayout()

        self.device_label = QLabel("Connected Devices:")
        self.device_combo = QComboBox()
        self.camera_label = QLabel("Camera Path:")
        self.camera_input = QLineEdit()
        self.camera_input.setReadOnly(True)

        self.target_label = QLabel("Target Folder (Dump Directory):")
        self.target_input = QLineEdit()
        self.browse_btn = QPushButton("Browse...")
        self.import_button = QPushButton("Import files")
        self.delete_button = QPushButton("Delete files")

        self.log_output = QTextEdit("Ready.\n")
        self.log_output.setReadOnly(True)

        self.main_layout.addWidget(self.device_label)
        self.main_layout.addWidget(self.device_combo)
        self.main_layout.addWidget(self.camera_label)
        self.main_layout.addWidget(self.camera_input)
        self.main_layout.addWidget(self.target_label)
        self.main_layout.addWidget(self.target_input)
        self.main_layout.addWidget(self.browse_btn)
        self.main_layout.addWidget(self.import_button)
        self.main_layout.addWidget(self.delete_button)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.log_output)

        self.setLayout(self.main_layout)
        self.resize(300, 100)

        # events
        self.browse_btn.clicked.connect(self.browse_target)
        self.device_combo.currentIndexChanged.connect(self.update_camera_path)
        self.import_button.clicked.connect(self.do_transfer)
        # self.delete_button.clicked.connect(self.handle_delete_button_click)

        self.populate_devices()

    def populate_devices(self):
        devices = get_connected_devices()
        self.device_combo.clear()
        for name, path, ctype in devices:
            display_name = f"{name} ({ctype})"
            self.device_combo.addItem(display_name, (path, ctype))

        if devices:
            self.device_combo.setCurrentIndex(0)
            self.update_camera_path(0)

    def update_camera_path(self, index):
        data = self.device_combo.itemData(index)
        if data:
            path, conn_type = data
            self.camera_input.setText(path)

    def browse_target(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Target Folder")
        if folder:
            self.target_input.setText(folder)

    def do_transfer(self):
        # Ignore if already running
        if self.thread and self.thread.isRunning():
            self.log_output.append("Transfer already in progress.")
            return

        data = self.device_combo.currentData()
        if not data:
            return

        camera_path, conn_type = data
        drafts_folder = self.target_input.text().strip()
        if not drafts_folder:
            QMessageBox.warning(
                self, "Warning", "Please select a target folder.")
            return

        self.import_button.setEnabled(False)
        self.log_output.append("Starting transfer...")

        if conn_type == "MTP":
            # Run MTP transfer directly on main thread (blocks UI)
            try:
                folder = move_files_from_mtp(
                    camera_path, drafts_folder, log_fn=self.log_output.append)
            except Exception as e:
                QMessageBox.critical(self, "Transfer Error", str(e))
            else:
                QMessageBox.information(
                    self, "Success", f"Files moved to:\n{folder}")
            self.import_button.setEnabled(True)

        else:
            # USB Mass Storage in background thread
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
