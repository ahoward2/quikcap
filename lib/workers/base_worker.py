import os
from PySide6.QtCore import QObject, Signal


class BaseWorker(QObject):
    progress = Signal(int)
    finished = Signal(str)
    error = Signal(str)
    log = Signal(str)

    def __init__(self):
        super().__init__()

    def count_files(self, folder: str) -> int:
        count = 0
        for _, _, files in os.walk(folder):
            count += len(files)
        return count

    def emit_finished(self, msg: str):
        self.finished.emit(msg)
        self.log.emit(f"[Finished] {msg}")

    def emit_error(self, msg: str):
        self.error.emit(msg)
        self.log.emit(f"[Error]: {msg}")
