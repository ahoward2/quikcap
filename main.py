# main.py
import sys
from typing import List
from lib.workers.transfer_worker import FileTransferWorker
from lib.workers.delete_worker import FileDeleteWorker
from lib.build_helpers import resource_path
from lib.file_ops import read_files_from_filesystem
from lib.file_ops import FileObject
from PySide6.QtCore import QThread, QSettings
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QLabel,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QFileDialog,
    QTextEdit,
    QMessageBox,
    QProgressBar,
    QTableWidgetItem,
)
from PySide6.QtGui import QIcon
from widgets.file_table import FileTable
from contants import SettingsKeys, UIStrings, DefaultWindowSize, InstructionsBoxSize


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.thread = None
        self.worker = None

        self.settings = QSettings(UIStrings.ORG_NAME, UIStrings.APP_NAME)

        self.setWindowTitle(UIStrings.APP_NAME)
        self.setWindowIcon(QIcon(resource_path("assets/favicon.ico")))
        self.main_layout = QVBoxLayout()
        self.content_layout = QHBoxLayout()
        self.left_content_layout = QVBoxLayout()
        self.center_content_layout = QVBoxLayout()
        self.right_content_layout = QVBoxLayout()
        self.bottom_layout = QHBoxLayout()
        self.bottom_left_layout = QVBoxLayout()
        self.bottom_right_layout = QVBoxLayout()

        self.camera_label = QLabel(UIStrings.CAMERA_PATH_LABEL)
        self.camera_input_row = QHBoxLayout()
        self.camera_input = QLineEdit()
        self.camera_browse_btn = QPushButton(UIStrings.BROWSE_BUTTON_LABEL)
        self.camera_input.setReadOnly(True)
        self.camera_input_row.addWidget(self.camera_browse_btn)
        self.camera_input_row.addWidget(self.camera_input)

        self.target_label = QLabel(UIStrings.TARGET_PATH_LABEL)
        self.target_input_row = QHBoxLayout()
        self.target_input = QLineEdit()
        self.target_input.setReadOnly(True)
        self.target_browse_btn = QPushButton(UIStrings.BROWSE_BUTTON_LABEL)
        self.target_input_row.addWidget(self.target_browse_btn)
        self.target_input_row.addWidget(self.target_input)

        self.actions_label = QLabel(UIStrings.ACTIONS_LABEL)
        self.import_button = QPushButton(UIStrings.IMPORT_BUTTON_LABEL)
        self.delete_button = QPushButton(UIStrings.DELETE_BUTTON_LABEL)

        self.source_preview_table = FileTable()
        self.source_preview_table.setMinimumHeight(200)
        self.source_preview_table.setMinimumWidth(300)
        self.source_preview_table.setEnabled(False)

        self.target_preview_table = FileTable()
        self.target_preview_table.setMinimumHeight(200)
        self.target_preview_table.setMinimumWidth(300)
        self.target_preview_table.setEnabled(False)

        # right layout widgets (not right layout yet)
        self.instructions_box = QTextEdit()
        self.instructions_box.setReadOnly(True)
        self.instructions_box.setMinimumHeight(InstructionsBoxSize.MIN_HEIGHT)
        self.instructions_box.setMinimumWidth(InstructionsBoxSize.MIN_WIDTH)

        # bottom layout widgets
        self.log_output = QTextEdit(UIStrings.READY_MSG)
        self.log_output.setReadOnly(True)
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setVisible(False)
        self.progress_bar.setValue(0)
        self.restore_settings()

        # Assemble left layout
        self.left_content_layout.addWidget(self.actions_label)
        self.left_content_layout.addWidget(self.create_horizontal_divider())
        self.left_content_layout.addWidget(self.import_button)
        self.left_content_layout.addWidget(self.delete_button)
        self.left_content_layout.addStretch()
        # Assemble center layout

        self.center_content_layout.addWidget(self.camera_label)
        self.center_content_layout.addWidget(self.create_horizontal_divider())
        self.center_content_layout.addLayout(self.camera_input_row)
        self.center_content_layout.addWidget(self.source_preview_table)

        # Assemble right layout
        self.right_content_layout.addWidget(self.target_label)
        self.right_content_layout.addWidget(self.create_horizontal_divider())
        self.right_content_layout.addLayout(self.target_input_row)
        self.right_content_layout.addWidget(self.target_preview_table)

        # Assemble bottom left layout
        self.bottom_left_layout.addWidget(self.log_output)
        self.bottom_left_layout.addWidget(self.progress_bar)

        # Assemble bottom right layout
        self.bottom_right_layout.addWidget(self.instructions_box)

        # Assemble bottom layout
        self.bottom_layout.addLayout(self.bottom_left_layout, stretch=5)
        self.bottom_layout.addLayout(self.bottom_right_layout, stretch=3)

        # Assemble layouts
        self.setLayout(self.main_layout)

        # Assemble content layout
        self.content_layout.addLayout(self.left_content_layout, stretch=2)
        self.content_layout.addLayout(self.center_content_layout, stretch=3)
        self.content_layout.addLayout(self.right_content_layout, stretch=3)

        self.main_layout.addLayout(self.content_layout)
        self.main_layout.addLayout(self.bottom_layout)

        self.resize(DefaultWindowSize.WIDTH, DefaultWindowSize.HEIGHT)

        self.camera_browse_btn.clicked.connect(self.browse_camera)
        self.target_browse_btn.clicked.connect(self.browse_target)
        self.import_button.clicked.connect(self.do_transfer)
        self.delete_button.clicked.connect(self.do_delete)

        self.load_instructions()
        self.update_source_preview_table()
        self.update_target_preview_table()

    def update_target_preview_table(self):
        target_path = self.target_input.text().strip()
        if not target_path:
            self.set_target_preview_table([])
            return

        try:
            files = read_files_from_filesystem(target_path)
            self.set_target_preview_table(files)
        except FileNotFoundError as e:
            self.log_output.append(
                f"Error reading files from target folder: {e}")
            self.set_target_preview_table([])

    def update_source_preview_table(self):
        camera_path = self.camera_input.text().strip()
        if not camera_path:
            self.set_source_preview_table([])
            return

        try:
            files = read_files_from_filesystem(camera_path)
            self.set_source_preview_table(files)
        except FileNotFoundError as e:
            self.log_output.append(
                f"Error reading files from camera folder: {e}")
            self.set_source_preview_table([])

    def set_target_preview_table(self, files: List[FileObject]):
        self.target_preview_table.clear_files()

        if not files:
            self.target_preview_table.setRowCount(1)
            newItem = QTableWidgetItem(UIStrings.FILES_NOT_FOUND_MSG)
            self.target_preview_table.setItem(0, 0, newItem)
            self.target_preview_table.setEnabled(False)
            return

        self.target_preview_table.setEnabled(True)

        for row, file in enumerate(files):
            self.target_preview_table.add_file(row=row, file=file)

    def set_source_preview_table(self, files: List[FileObject]):
        self.source_preview_table.clear_files()

        if not files:
            self.source_preview_table.setRowCount(1)
            newItem = QTableWidgetItem(UIStrings.FILES_NOT_FOUND_MSG)
            self.source_preview_table.setItem(0, 0, newItem)
            self.source_preview_table.setEnabled(False)
            return

        self.source_preview_table.setEnabled(True)

        for row, file in enumerate(files):
            self.source_preview_table.add_file(row=row, file=file)

    def create_horizontal_divider(self):
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        return divider

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
            self.update_source_preview_table()

    def browse_target(self):
        initial_path = self.target_input.text().strip() or ""
        folder = QFileDialog.getExistingDirectory(
            self, UIStrings.TARGET_DIR_CAPTION, initial_path)
        if folder:
            self.target_input.setText(folder)
            self.settings.setValue(SettingsKeys.TARGET_PATH, folder)
            self.update_target_preview_table()

    def do_transfer(self):
        if self.thread and self.thread.isRunning():
            self.log_output.append(UIStrings.TASK_ALREADY_RUNNING_MSG)
            return

        camera_path = self.camera_input.text().strip()
        drafts_folder = self.target_input.text().strip()

        if not drafts_folder:
            QMessageBox.warning(
                self, "Warning", UIStrings.TARGET_FOLDER_NOT_SET_MSG)
            return

        self.switch_action_buttons(False)

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

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.finished.connect(self.on_thread_finished)

        self.thread.start()

    def on_transfer_complete(self, folder):
        self.update_target_preview_table()
        self.update_source_preview_table()
        QMessageBox.information(
            self, "Transfer Complete", UIStrings.FILES_MOVED_MSG.format(folder))

    def on_transfer_error(self, error_msg):
        self.log_output.append(UIStrings.TRANSFER_ERROR_MSG.format(error_msg))
        self.progress_bar.setVisible(False)
        QMessageBox.critical(self, "Transfer Error",
                             UIStrings.TRANSFER_ERROR_MSG.format(error_msg))

    def do_delete(self):
        if self.thread and self.thread.isRunning():
            self.log_output.append(UIStrings.TASK_ALREADY_RUNNING_MSG)
            return

        target_path = self.camera_input.text().strip()
        if not target_path:
            QMessageBox.warning(
                self, "Warning", UIStrings.TARGET_FOLDER_NOT_SET_MSG)
            return

        self.switch_action_buttons(False)

        self.thread = QThread()
        self.worker = FileDeleteWorker(target_path)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)

        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_delete_complete)
        self.worker.error.connect(self.on_delete_error)
        self.worker.log.connect(self.log_output.append)

        # Clean up
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.on_thread_finished)

        self.thread.start()

    def on_delete_complete(self, folder):
        self.update_source_preview_table()
        QMessageBox.information(self, "Deletion Complete",
                                UIStrings.FILES_DELETED_MSG.format(folder))

    def on_delete_error(self, error_msg):
        self.log_output.append(UIStrings.DELETE_ERROR_MSG.format(error_msg))
        self.progress_bar.setVisible(False)
        QMessageBox.critical(self, "Delete Error",
                             UIStrings.DELETE_ERROR_MSG.format(error_msg))

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

    def load_instructions(self):
        try:
            with open(resource_path("assets/instructions.html"), "r", encoding="utf-8") as f:
                self.instructions_box.setHtml(f.read())
        except Exception as e:
            self.instructions_box.setText("Instructions could not be loaded.")
            print(f"Failed to load instructions.html: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
