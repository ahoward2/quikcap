from PySide6.QtCore import Qt, QUrl
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
from PySide6.QtGui import QDesktopServices
from lib.file_ops import FileObject
import os


class FileTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._name_column = 0
        self._size_column = 1
        self._path_column = 2
        self.setColumnCount(3)
        self.setColumnHidden(self._path_column, True)  # hide paths from ui
        self.setHorizontalHeaderLabels(['Name', 'Size', 'Path'])
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)

        self.cellDoubleClicked.connect(self._on_cell_double_clicked)

    def _on_cell_double_clicked(self, row, column):
        """
        Handle double-click on a cell to open the file in the default application.
        """
        path_item = self.item(row, self._path_column)
        if path_item:
            file_path = path_item.text()
            if os.path.isfile(file_path):
                QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))
            else:
                QMessageBox.warning(self, "File Not Found",
                                    f"The file '{file_path}' does not exist.")

    def add_file(self, row, file: FileObject):
        self.insertRow(row)
        name_item = QTableWidgetItem(file.name)
        size_item = QTableWidgetItem(file.size)
        path_item = QTableWidgetItem(file.path)
        self.setItem(row, self._name_column, name_item)
        self.setItem(row, self._size_column, size_item)
        self.setItem(row, self._path_column, path_item)
        name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
        size_item.setFlags(size_item.flags() & ~Qt.ItemIsEditable)
        size_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        path_item.setFlags(path_item.flags() & ~Qt.ItemIsEditable)

    def clear_files(self):
        self.setRowCount(0)
