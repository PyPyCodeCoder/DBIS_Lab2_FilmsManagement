from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QWidget, QLineEdit
from film import Film
from studio import Studio
from genre import Genre
from custom_input_dialog import CustomInputDialog


class FilmManager(QWidget):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.film_manager = Film(self.connection)
        self.studio_manager = Studio(self.connection)
        self.genre_manager = Genre(self.connection)

        self.layout = QVBoxLayout()
        self.film_table = QTableWidget()
        self.layout.addWidget(self.film_table)

        self.add_film_button = QPushButton("Add Film")
        self.add_film_button.clicked.connect(self.add_film)
        self.layout.addWidget(self.add_film_button)

        self.update_film_button = QPushButton("Update Film")
        self.update_film_button.clicked.connect(self.update_film)
        self.layout.addWidget(self.update_film_button)

        self.delete_film_button = QPushButton("Delete Film")
        self.delete_film_button.clicked.connect(self.delete_film)
        self.layout.addWidget(self.delete_film_button)

        self.setLayout(self.layout)
        self.load_films()

    def load_films(self):
        films = self.film_manager.read_films()
        self.film_table.setRowCount(len(films))
        self.film_table.setColumnCount(9)
        self.film_table.setHorizontalHeaderLabels(
            ["ID", "Name", "Description", "Release Date", "Language", "Duration", "Budget", "Studio", "Genre"])

        for row_idx, row_data in enumerate(films):
            for col_idx, col_data in enumerate(row_data):
                self.film_table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

    def add_film(self):
        name, ok = CustomInputDialog.getText(self, "Add Film", "Film Name:")
        if not ok or not name:
            return

        description, ok = CustomInputDialog.getText(self, "Add Film", "Description:")
        if not ok:
            return

        release_date, ok = CustomInputDialog.getText(self, "Add Film", "Release Date (YYYY-MM-DD):")
        if not ok:
            return
        is_valid, message = self.film_manager.validate_film_details(name, description, release_date, '', '', 1)
        if not is_valid:
            QMessageBox.warning(self, "Error", message)
            return

        language, ok = CustomInputDialog.getText(self, "Add Film", "Language:")
        if not ok:
            return

        duration, ok = CustomInputDialog.getText(self, "Add Film", "Duration (HH:MM:SS):")
        if not ok:
            return
        is_valid, message = self.film_manager.validate_film_details(name, description, release_date, language, duration,
                                                                    1)
        if not is_valid:
            QMessageBox.warning(self, "Error", message)
            return

        budget, ok = CustomInputDialog.getInt(self, "Add Film", "Budget:")
        if not ok or budget <= 0:
            QMessageBox.warning(self, "Error", "Budget must be a positive number.")
            return

        studios = self.studio_manager.read_studios()
        studio_names = [studio[1] for studio in studios]
        studio_name, ok = CustomInputDialog.getItem(self, "Add Film", "Select Studio:", studio_names, 0, False)
        if not ok or not studio_name:
            return
        studio_id = [studio[0] for studio in studios if studio[1] == studio_name][0]

        genres = self.genre_manager.read_genres()
        genre_names = [genre[1] for genre in genres]
        genre_name, ok = CustomInputDialog.getItem(self, "Add Film", "Select Genre:", genre_names, 0, False)
        if not ok or not genre_name:
            return
        genre_id = [genre[0] for genre in genres if genre[1] == genre_name][0]

        success, message = self.film_manager.create_film(name, description, release_date, language, duration, budget,
                                                         studio_id, genre_id)
        if not success:
            QMessageBox.warning(self, "Error", message)
        else:
            self.load_films()

    def update_film(self):
        selected_items = self.film_table.selectedItems()
        if not selected_items:
            return

        try:
            film_id = int(selected_items[0].text())
            new_name, ok = CustomInputDialog.getText(self, "Update Film", "New Film Name:", QLineEdit.Normal,
                                                     selected_items[1].text())
            if not ok or not new_name:
                return

            new_description, ok = CustomInputDialog.getText(self, "Update Film", "New Description:", QLineEdit.Normal,
                                                            selected_items[2].text())
            if not ok:
                return

            new_release_date, ok = CustomInputDialog.getText(self, "Update Film", "New Release Date (YYYY-MM-DD):",
                                                             QLineEdit.Normal, selected_items[3].text())
            if not ok:
                return
            is_valid, message = self.film_manager.validate_film_details(new_name, new_description, new_release_date, '',
                                                                        '', 1)
            if not is_valid:
                QMessageBox.warning(self, "Error", message)
                return

            new_language, ok = CustomInputDialog.getText(self, "Update Film", "New Language:", QLineEdit.Normal,
                                                         selected_items[4].text())
            if not ok:
                return

            new_duration, ok = CustomInputDialog.getText(self, "Update Film", "New Duration (HH:MM:SS):",
                                                         QLineEdit.Normal, selected_items[5].text())
            if not ok:
                return
            is_valid, message = self.film_manager.validate_film_details(new_name, new_description, new_release_date,
                                                                        new_language, new_duration, 1)
            if not is_valid:
                QMessageBox.warning(self, "Error", message)
                return

            new_budget, ok = CustomInputDialog.getInt(self, "Update Film", "New Budget:", int(selected_items[6].text()))
            if not ok or new_budget <= 0:
                QMessageBox.warning(self, "Error", "Budget must be a positive number.")
                return

            current_studio_name = selected_items[7].text()
            studios = self.studio_manager.read_studios()
            studio_names = [studio[1] for studio in studios]

            if current_studio_name not in studio_names:
                raise ValueError(f"Studio name '{current_studio_name}' not found in studios list.")
            studio_index = studio_names.index(current_studio_name)
            new_studio_name, ok = CustomInputDialog.getItem(self, "Update Film", "Select Studio:", studio_names,
                                                            studio_index, False)
            if not ok or not new_studio_name:
                return
            new_studio_id = [studio[0] for studio in studios if studio[1] == new_studio_name][0]

            current_genre_name = selected_items[8].text()
            genres = self.genre_manager.read_genres()
            genre_names = [genre[1] for genre in genres]

            if current_genre_name not in genre_names:
                raise ValueError(f"Genre name '{current_genre_name}' not found in genres list.")
            genre_index = genre_names.index(current_genre_name)
            new_genre_name, ok = CustomInputDialog.getItem(self, "Update Film", "Select Genre:",
                                                           genre_names, genre_index, False)
            if not ok or not new_genre_name:
                return
            new_genre_id = [genre[0] for genre in genres if genre[1] == new_genre_name][0]

            success, message = self.film_manager.update_film(film_id, new_name, new_description, new_release_date,
                                                             new_language, new_duration, new_budget, new_studio_id,
                                                             new_genre_id)
            if not success:
                QMessageBox.warning(self, "Error", message)
            else:
                self.load_films()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def delete_film(self):
        selected_items = self.film_table.selectedItems()
        if not selected_items:
            return

        film_id = int(selected_items[0].text())
        confirm = QMessageBox.question(self, "Delete Film", "Are you sure you want to delete this film?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.film_manager.delete_film(film_id)
            self.load_films()
