from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QWidget, QLineEdit
from custom_input_dialog import CustomInputDialog
from genre import Genre


class GenreManager(QWidget):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.genre_manager = Genre(self.connection)

        self.layout = QVBoxLayout()
        self.genre_table = QTableWidget()
        self.layout.addWidget(self.genre_table)

        self.add_genre_button = QPushButton("Add Genre")
        self.add_genre_button.clicked.connect(self.add_genre)
        self.layout.addWidget(self.add_genre_button)

        self.update_genre_button = QPushButton("Update Genre")
        self.update_genre_button.clicked.connect(self.update_genre)
        self.layout.addWidget(self.update_genre_button)

        self.delete_genre_button = QPushButton("Delete Genre")
        self.delete_genre_button.clicked.connect(self.delete_genre)
        self.layout.addWidget(self.delete_genre_button)

        self.setLayout(self.layout)
        self.load_genres()

    def load_genres(self):
        genres = self.genre_manager.read_genres()
        self.genre_table.setRowCount(len(genres))
        self.genre_table.setColumnCount(2)
        self.genre_table.setHorizontalHeaderLabels(["ID", "Name"])

        for row_idx, row_data in enumerate(genres):
            self.genre_table.setItem(row_idx, 0, QTableWidgetItem(str(row_data[0])))
            self.genre_table.setItem(row_idx, 1, QTableWidgetItem(row_data[1]))

    def add_genre(self):
        name, ok = CustomInputDialog.getText(self, "Add Genre", "Genre Name:")
        if ok and name:
            self.genre_manager.create_genre(name)
            self.load_genres()

    def update_genre(self):
        selected_items = self.genre_table.selectedItems()
        if selected_items:
            genre_id = int(selected_items[0].text())
            new_name, ok = CustomInputDialog.getText(self, "Update Genre", "New Genre Name:", QLineEdit.Normal,
                                                     selected_items[1].text())
            if ok and new_name:
                self.genre_manager.update_genre(genre_id, new_name)
                self.load_genres()

    def delete_genre(self):
        selected_items = self.genre_table.selectedItems()
        if selected_items:
            genre_id = int(selected_items[0].text())
            confirm = QMessageBox.question(self, "Delete Genre", "Are you sure you want to delete this genre?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if confirm == QMessageBox.Yes:
                self.genre_manager.delete_genre(genre_id)
                self.load_genres()
