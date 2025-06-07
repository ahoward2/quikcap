from lib.workers.base_worker import BaseWorker
from lib.file_ops import delete_files_from_filesystem
from contants import UIStrings


class FileDeleteWorker(BaseWorker):
    def __init__(self, target_path):
        super().__init__()
        self.target_path = target_path

    def run(self):
        try:
            self.log.emit(UIStrings.STARTING_FILE_DELETION_MSG)
            self.total_files = self.count_files(self.target_path)
            if self.total_files == 0:
                self.emit_finished(UIStrings.FILES_NOT_FOUND_MSG)
                return
            self.log.emit(UIStrings.FILES_FOUND_MSG.format(self.total_files))
            self.log.emit(UIStrings.DELETING_FILES_MSG)
            result = delete_files_from_filesystem(
                self.target_path, self.progress.emit)
            self.emit_finished(UIStrings.FILES_DELETED_MSG.format(result))
        except Exception as e:
            self.emit_error(str(e))
