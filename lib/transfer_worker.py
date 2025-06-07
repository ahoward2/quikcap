from PySide6.QtCore import QObject, Signal
from lib.file_ops import move_files_from_filesystem
import os


class FileTransferWorker(QObject):
    progress = Signal(int)
    finished = Signal(str)
    error = Signal(str)
    log = Signal(str)

    def __init__(self, camera_path, target_path):
        super().__init__()
        self.camera_path = camera_path
        self.target_path = target_path

    def _count_files(self, folder):
        count = 0
        for _, _, files in os.walk(folder):
            count += len(files)
        return count

    def run(self):
        try:
            self.log.emit("Starting USB Mass Storage transfer...")
            self.total_files = self._count_files(self.camera_path)
            self.copied_files = 0
            if self.total_files == 0:
                self.log.emit("No files found to transfer.")
                self.finished.emit("No files to transfer.")
                return
            self.log.emit(f"Found {self.total_files} files to transfer.")
            self.log.emit("Transferring files...")
            result = move_files_from_filesystem(
                self.camera_path, self.target_path, self.progress.emit)
            self.log.emit("Transfer complete.")
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))
