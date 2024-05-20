from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QWidget, QLineEdit
from worker import Worker
from datetime import datetime
import re
from custom_input_dialog import CustomInputDialog


class WorkerManager(QWidget):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.worker_manager = Worker(self.connection)

        self.layout = QVBoxLayout()
        self.worker_table = QTableWidget()
        self.layout.addWidget(self.worker_table)

        self.add_worker_button = QPushButton("Add Worker")
        self.add_worker_button.clicked.connect(self.add_worker)
        self.layout.addWidget(self.add_worker_button)

        self.update_worker_button = QPushButton("Update Worker")
        self.update_worker_button.clicked.connect(self.update_worker)
        self.layout.addWidget(self.update_worker_button)

        self.delete_worker_button = QPushButton("Delete Worker")
        self.delete_worker_button.clicked.connect(self.delete_worker)
        self.layout.addWidget(self.delete_worker_button)

        self.setLayout(self.layout)
        self.load_workers()

    def load_workers(self):
        workers = self.worker_manager.read_workers()
        self.worker_table.setRowCount(len(workers))
        self.worker_table.setColumnCount(4)
        self.worker_table.setHorizontalHeaderLabels(["ID", "Name", "Birth Date", "Nationality"])

        for row_idx, row_data in enumerate(workers):
            self.worker_table.setItem(row_idx, 0, QTableWidgetItem(str(row_data[0])))
            self.worker_table.setItem(row_idx, 1, QTableWidgetItem(row_data[1]))
            self.worker_table.setItem(row_idx, 2, QTableWidgetItem(row_data[2]))
            self.worker_table.setItem(row_idx, 3, QTableWidgetItem(row_data[3]))

    def add_worker(self):
        name, ok = CustomInputDialog.getText(self, "Add Worker", "Worker Name:")
        if ok and name:
            birth_date, ok = CustomInputDialog.getText(self, "Add Worker", "Birth Date (YYYY-MM-DD):")
            if ok and birth_date:
                if not re.match(r'\d{4}-\d{2}-\d{2}', birth_date):
                    QMessageBox.warning(self, "Invalid Date Format",
                                        "Please enter the birth date in the format YYYY-MM-DD.")
                    return

                try:
                    datetime.strptime(birth_date, '%Y-%m-%d')
                except ValueError:
                    QMessageBox.warning(self, "Invalid Date", "Please enter a valid birth date.")
                    return

                nationality, ok = CustomInputDialog.getText(self, "Add Worker", "Nationality:")
                if ok and nationality:
                    self.worker_manager.create_worker(name, birth_date, nationality)
                    self.load_workers()

    def update_worker(self):
        selected_items = self.worker_table.selectedItems()
        if selected_items:
            worker_id = int(selected_items[0].text())
            new_name, ok = CustomInputDialog.getText(self, "Update Worker", "New Worker Name:", QLineEdit.Normal,
                                                     selected_items[1].text())
            if ok and new_name:
                new_birth_date, ok = CustomInputDialog.getText(self, "Update Worker", "New Birth Date (YYYY-MM-DD):",
                                                               QLineEdit.Normal, selected_items[2].text())
                if ok and new_birth_date:
                    if not re.match(r'\d{4}-\d{2}-\d{2}', new_birth_date):
                        QMessageBox.warning(self, "Invalid Date Format",
                                            "Please enter the birth date in the format YYYY-MM-DD.")
                        return

                    try:
                        datetime.strptime(new_birth_date, '%Y-%m-%d')
                    except ValueError:
                        QMessageBox.warning(self, "Invalid Date", "Please enter a valid birth date.")
                        return

                    new_nationality, ok = CustomInputDialog.getText(self, "Update Worker", "New Nationality:",
                                                                    QLineEdit.Normal, selected_items[3].text())
                    if ok and new_nationality:
                        self.worker_manager.update_worker(worker_id, new_name, new_birth_date, new_nationality)
                        self.load_workers()

    def delete_worker(self):
        selected_items = self.worker_table.selectedItems()
        if selected_items:
            worker_id = int(selected_items[0].text())
            confirm = QMessageBox.question(self, "Delete Worker", "Are you sure you want to delete this worker?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if confirm == QMessageBox.Yes:
                self.worker_manager.delete_worker(worker_id)
                self.load_workers()
