from contants import UIStrings
from lib.file_ops import move_files_from_filesystem
from lib.workers.base_worker import BaseWorker


class FileTransferWorker(BaseWorker):
    def __init__(self, camera_path, target_path):
        super().__init__()
        self.camera_path = camera_path
        self.target_path = target_path

    def run(self):
        try:
            self.log.emit(UIStrings.START_USB_TRANSFER_MSG)
            self.total_files = self.count_files(self.camera_path)
            self.copied_files = 0
            if self.total_files == 0:
                self.emit_finished(UIStrings.FILES_NOT_FOUND_MSG)
                return
            self.log.emit(UIStrings.FILES_FOUND_MSG.format(self.total_files))
            self.log.emit(UIStrings.TRANSFERRING_FILES_MSG)
            result = move_files_from_filesystem(
                self.camera_path, self.target_path, self.progress.emit)
            self.emit_finished(UIStrings.FILES_MOVED_MSG.format(result))
        except Exception as e:
            self.emit_error(str(e))
