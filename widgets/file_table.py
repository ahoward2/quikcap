from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView


class FileTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(['File Name', 'Size'])
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)

    def add_file(self, row, file_name, size):
        self.insertRow(row)
        name_item = QTableWidgetItem(file_name)
        size_item = QTableWidgetItem(size)
        name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
        size_item.setFlags(size_item.flags() & ~Qt.ItemIsEditable)
        size_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.setItem(row, 0, QTableWidgetItem(file_name))
        self.setItem(row, 1, QTableWidgetItem(str(size)))

    def clear_files(self):
        self.setRowCount(0)
