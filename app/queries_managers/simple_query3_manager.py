from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QMessageBox


class SimpleQuery3Manager(QWidget):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.studio_combo_box = QComboBox()
        self.populate_studios()
        self.layout.addWidget(self.studio_combo_box)

        self.query_button = QPushButton("Get Countries where a specific Studio worked")
        self.query_button.clicked.connect(self.execute_query)
        self.layout.addWidget(self.query_button)

        self.result_table = QTableWidget()
        self.layout.addWidget(self.result_table)

    def populate_studios(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM Studio")
        studios = cursor.fetchall()
        self.studio_combo_box.addItems([studio[0] for studio in studios])

    def execute_query(self):
        studio_name = self.studio_combo_box.currentText()
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT DISTINCT Country.country_id, Country.name
            FROM Country
            JOIN FilmCountries ON Country.country_id = FilmCountries.country_id
            JOIN Film ON FilmCountries.film_id = Film.film_id
            JOIN Studio ON Film.studio_id = Studio.studio_id
            WHERE Studio.name = ?
        """, (studio_name,))
        rows = cursor.fetchall()

        if rows:
            self.result_table.setRowCount(len(rows))
            self.result_table.setColumnCount(2)
            self.result_table.setHorizontalHeaderLabels(["ID", "Name"])

            for row_idx, row_data in enumerate(rows):
                for col_idx, col_data in enumerate(row_data):
                    self.result_table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        else:
            QMessageBox.information(self, "No results", "No countries found where the selected studio worked.")
