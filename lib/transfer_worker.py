from PySide6.QtCore import QObject, Signal
from lib.import_files import move_files_from_filesystem


class FileTransferWorker(QObject):
    finished = Signal(str)
    error = Signal(str)
    log = Signal(str)

    def __init__(self, camera_path, target_path):
        super().__init__()
        self.camera_path = camera_path
        self.target_path = target_path

    def run(self):
        try:
            self.log.emit("Starting USB Mass Storage transfer...")
            result = move_files_from_filesystem(
                self.camera_path, self.target_path)
            self.log.emit("Transfer complete.")
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))
