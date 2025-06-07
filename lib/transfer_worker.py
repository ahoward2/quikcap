from PySide6.QtCore import QObject, Signal
from lib.file_ops import move_files_from_filesystem
import os
from contants import UIStrings


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
            self.log.emit(UIStrings.START_USB_TRANSFER_MSG)
            self.total_files = self._count_files(self.camera_path)
            self.copied_files = 0
            if self.total_files == 0:
                self.log.emit(UIStrings.FILES_NOT_FOUND_MSG)
                self.finished.emit(UIStrings.FILES_NOT_FOUND_MSG)
                return
            self.log.emit(UIStrings.FILES_FOUND_MSG.format(self.total_files))
            self.log.emit(UIStrings.TRANSFERRING_FILES_MSG)
            result = move_files_from_filesystem(
                self.camera_path, self.target_path, self.progress.emit)
            self.log.emit(UIStrings.TRANSFER_COMPLETE_MSG)
            self.log.emit(UIStrings.FILES_MOVED_MSG.format(result))
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))
