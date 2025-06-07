# main.py
import sys
from lib.transfer_worker import FileTransferWorker
from PySide6.QtCore import QThread, QSettings
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QFileDialog,
    QTextEdit,
    QMessageBox,
    QProgressBar,
)
from contants import SettingsKeys, UIStrings, DefaultWindowSize


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.thread = None
        self.worker = None

        self.settings = QSettings(UIStrings.ORG_NAME, UIStrings.APP_NAME)

        self.setWindowTitle(UIStrings.APP_NAME)
        self.main_layout = QVBoxLayout()

        self.camera_label = QLabel(UIStrings.CAMERA_PATH_LABEL)
        self.camera_input = QLineEdit()
        self.camera_browse_btn = QPushButton(UIStrings.BROWSE_BUTTON_LABEL)
        self.camera_input.setReadOnly(True)
        self.target_label = QLabel(UIStrings.TARGET_PATH_LABEL)
        self.target_input = QLineEdit()
        self.target_input.setReadOnly(True)
        self.target_browse_btn = QPushButton(UIStrings.BROWSE_BUTTON_LABEL)
        self.import_button = QPushButton(UIStrings.IMPORT_BUTTON_LABEL)
        self.delete_button = QPushButton(UIStrings.DELETE_BUTTON_LABEL)
        self.log_output = QTextEdit(UIStrings.READY_MSG)
        self.log_output.setReadOnly(True)
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setVisible(False)
        self.progress_bar.setValue(0)

        self.restore_settings()

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
        self.main_layout.addWidget(self.progress_bar)

        self.setLayout(self.main_layout)
        self.resize(DefaultWindowSize.WIDTH, DefaultWindowSize.HEIGHT)

        self.camera_browse_btn.clicked.connect(self.browse_camera)
        self.target_browse_btn.clicked.connect(self.browse_target)
        self.import_button.clicked.connect(self.do_transfer)
        # self.delete_button.clicked.connect(self.handle_delete_button_click)

    def switch_action_buttons(self, enable: bool):
        self.import_button.setEnabled(enable)
        self.delete_button.setEnabled(enable)

    def restore_settings(self):
        camera_path = self.settings.value(SettingsKeys.CAMERA_PATH, "")
        target_path = self.settings.value(SettingsKeys.TARGET_PATH, "")

        if camera_path:
            self.camera_input.setText(camera_path)
        if target_path:
            self.target_input.setText(target_path)

    def browse_camera(self):
        initial_path = self.camera_input.text().strip() or ""
        folder = QFileDialog.getExistingDirectory(
            self, UIStrings.CAMERA_DIR_CAPTION, initial_path)
        if folder:
            self.camera_input.setText(folder)
            self.settings.setValue(SettingsKeys.CAMERA_PATH, folder)

    def browse_target(self):
        initial_path = self.target_input.text().strip() or ""
        folder = QFileDialog.getExistingDirectory(
            self, UIStrings.TARGET_DIR_CAPTION, initial_path)
        if folder:
            self.target_input.setText(folder)
            self.settings.setValue(SettingsKeys.TARGET_PATH, folder)

    def do_transfer(self):
        if self.thread and self.thread.isRunning():
            self.log_output.append(UIStrings.TRANSFER_ALREADY_RUNNING_MSG)
            return

        camera_path = self.camera_input.text().strip()
        drafts_folder = self.target_input.text().strip()

        if not drafts_folder:
            QMessageBox.warning(
                self, "Warning", UIStrings.TARGET_FOLDER_NOT_SET_MSG)
            return

        self.switch_action_buttons(False)
        self.log_output.append(UIStrings.STARTING_TRANSFER_MSG)

        self.thread = QThread()
        self.worker = FileTransferWorker(camera_path, drafts_folder)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setVisible(True)

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
        QMessageBox.information(
            self, "Transfer Complete", UIStrings.FILES_MOVED_MSG.format(folder))

    def on_transfer_error(self, error_msg):
        self.log_output.append(UIStrings.TRANSFER_ERROR_MSG.format(error_msg))
        self.progress_bar.setVisible(False)
        QMessageBox.critical(self, "Transfer Error", error_msg)

    def on_thread_finished(self):
        self.progress_bar.setVisible(False)
        self.switch_action_buttons(True)
        self.thread = None
        self.worker = None

    def closeEvent(self, event):
        if self.thread and self.thread.isRunning():
            self.log_output.append(UIStrings.WAIT_FOR_CLOSE_MSG)
            self.thread.quit()
            self.thread.wait()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
