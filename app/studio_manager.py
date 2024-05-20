from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QWidget, QLineEdit
from studio import Studio
from custom_input_dialog import CustomInputDialog


class StudioManager(QWidget):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.studio_manager = Studio(self.connection)

        self.layout = QVBoxLayout()
        self.studio_table = QTableWidget()
        self.layout.addWidget(self.studio_table)

        self.add_studio_button = QPushButton("Add Studio")
        self.add_studio_button.clicked.connect(self.add_studio)
        self.layout.addWidget(self.add_studio_button)

        self.update_studio_button = QPushButton("Update Studio")
        self.update_studio_button.clicked.connect(self.update_studio)
        self.layout.addWidget(self.update_studio_button)

        self.delete_studio_button = QPushButton("Delete Studio")
        self.delete_studio_button.clicked.connect(self.delete_studio)
        self.layout.addWidget(self.delete_studio_button)

        self.setLayout(self.layout)
        self.load_studios()

    def load_studios(self):
        studios = self.studio_manager.read_studios()
        self.studio_table.setRowCount(len(studios))
        self.studio_table.setColumnCount(2)
        self.studio_table.setHorizontalHeaderLabels(["ID", "Name"])

        for row_idx, row_data in enumerate(studios):
            self.studio_table.setItem(row_idx, 0, QTableWidgetItem(str(row_data[0])))
            self.studio_table.setItem(row_idx, 1, QTableWidgetItem(row_data[1]))

    def add_studio(self):
        name, ok = CustomInputDialog.getText(self, "Add Studio", "Studio Name:")
        if ok and name:
            self.studio_manager.create_studio(name)
            self.load_studios()

    def update_studio(self):
        selected_items = self.studio_table.selectedItems()
        if selected_items:
            studio_id = int(selected_items[0].text())
            new_name, ok = CustomInputDialog.getText(self, "Update Studio", "New Studio Name:", QLineEdit.Normal,
                                                     selected_items[1].text())
            if ok and new_name:
                self.studio_manager.update_studio(studio_id, new_name)
                self.load_studios()

    def delete_studio(self):
        selected_items = self.studio_table.selectedItems()
        if selected_items:
            studio_id = int(selected_items[0].text())
            confirm = QMessageBox.question(self, "Delete Studio", "Are you sure you want to delete this studio?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if confirm == QMessageBox.Yes:
                self.studio_manager.delete_studio(studio_id)
                self.load_studios()
