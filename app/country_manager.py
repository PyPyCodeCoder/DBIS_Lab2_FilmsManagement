from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QWidget, QLineEdit
from country import Country
from custom_input_dialog import CustomInputDialog


class CountryManager(QWidget):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.country_manager = Country(self.connection)

        self.layout = QVBoxLayout()
        self.country_table = QTableWidget()
        self.layout.addWidget(self.country_table)

        self.add_country_button = QPushButton("Add Country")
        self.add_country_button.clicked.connect(self.add_country)
        self.layout.addWidget(self.add_country_button)

        self.update_country_button = QPushButton("Update Country")
        self.update_country_button.clicked.connect(self.update_country)
        self.layout.addWidget(self.update_country_button)

        self.delete_country_button = QPushButton("Delete Country")
        self.delete_country_button.clicked.connect(self.delete_country)
        self.layout.addWidget(self.delete_country_button)

        self.setLayout(self.layout)
        self.load_countries()

    def load_countries(self):
        countries = self.country_manager.read_countries()
        self.country_table.setRowCount(len(countries))
        self.country_table.setColumnCount(2)
        self.country_table.setHorizontalHeaderLabels(["ID", "Name"])

        for row_idx, row_data in enumerate(countries):
            self.country_table.setItem(row_idx, 0, QTableWidgetItem(str(row_data[0])))
            self.country_table.setItem(row_idx, 1, QTableWidgetItem(row_data[1]))

    def add_country(self):
        name, ok = CustomInputDialog.getText(self, "Add Country", "Country Name:")
        if ok and name:
            self.country_manager.create_country(name)
            self.load_countries()

    def update_country(self):
        selected_items = self.country_table.selectedItems()
        if selected_items:
            country_id = int(selected_items[0].text())
            new_name, ok = CustomInputDialog.getText(self, "Update Country", "New Country Name:", QLineEdit.Normal,
                                                     selected_items[1].text())
            if ok and new_name:
                self.country_manager.update_country(country_id, new_name)
                self.load_countries()

    def delete_country(self):
        selected_items = self.country_table.selectedItems()
        if selected_items:
            country_id = int(selected_items[0].text())
            confirm = QMessageBox.question(self, "Delete Country", "Are you sure you want to delete this country?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if confirm == QMessageBox.Yes:
                self.country_manager.delete_country(country_id)
                self.load_countries()
