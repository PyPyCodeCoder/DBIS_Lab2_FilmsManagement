from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QWidget
from film_country import FilmCountry
from film import Film
from country import Country
from custom_input_dialog import CustomInputDialog


class FilmCountryManager(QWidget):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.film_country_manager = FilmCountry(self.connection)
        self.film_manager = Film(self.connection)
        self.country_manager = Country(self.connection)

        self.layout = QVBoxLayout()
        self.film_country_table = QTableWidget()
        self.layout.addWidget(self.film_country_table)

        self.add_film_country_button = QPushButton("Add Film Country")
        self.add_film_country_button.clicked.connect(self.add_film_country)
        self.layout.addWidget(self.add_film_country_button)

        self.delete_film_country_button = QPushButton("Delete Film Country")
        self.delete_film_country_button.clicked.connect(self.delete_film_country)
        self.layout.addWidget(self.delete_film_country_button)

        self.setLayout(self.layout)
        self.load_film_countries()

    def load_film_countries(self):
        film_countries = self.film_country_manager.read_film_countries()
        self.film_country_table.setRowCount(len(film_countries))
        self.film_country_table.setColumnCount(4)
        self.film_country_table.setHorizontalHeaderLabels(["ID", "Film", "Country", "Description"])

        for row_idx, row_data in enumerate(film_countries):
            for col_idx, col_data in enumerate(row_data):
                self.film_country_table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

    def add_film_country(self):
        films = self.film_manager.read_films()
        film_names = [film[1] for film in films]
        film_name, ok = CustomInputDialog.getItem(self, "Add Film Country", "Select Film:", film_names, 0, False)
        if ok and film_name:
            film_id = [film[0] for film in films if film[1] == film_name][0]

            countries = self.country_manager.read_countries()
            country_names = [country[1] for country in countries]
            country_name, ok = CustomInputDialog.getItem(self, "Add Film Country", "Select Country:",
                                                         country_names, 0, False)
            if ok and country_name:
                country_id = [country[0] for country in countries if country[1] == country_name][0]

                description, ok = CustomInputDialog.getText(self, "Add Film Country", "Description:")
                if ok and description:
                    self.film_country_manager.create_film_country(film_id, country_id, description)
                    self.load_film_countries()

    def delete_film_country(self):
        selected_items = self.film_country_table.selectedItems()
        if selected_items:
            film_countries_id = int(selected_items[0].text())
            confirm = QMessageBox.question(self, "Delete Film Country",
                                           "Are you sure you want to delete this film country?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if confirm == QMessageBox.Yes:
                self.film_country_manager.delete_film_country(film_countries_id)
                self.load_film_countries()
