from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QMessageBox


class ComplexQuery1Manager(QWidget):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.film_combo_box = QComboBox()
        self.populate_films()
        self.film_combo_box.currentIndexChanged.connect(self.populate_actors)
        self.layout.addWidget(self.film_combo_box)

        self.actor_combo_box = QComboBox()
        self.layout.addWidget(self.actor_combo_box)

        self.query_button = QPushButton("Find Actors filming in same Countries")
        self.query_button.clicked.connect(self.execute_query)
        self.layout.addWidget(self.query_button)

        self.result_table = QTableWidget()
        self.layout.addWidget(self.result_table)

        self.populate_actors()

    def populate_films(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM Film")
        films = cursor.fetchall()
        self.film_combo_box.addItems([film[0] for film in films])

    def populate_actors(self):
        self.actor_combo_box.clear()
        film_name = self.film_combo_box.currentText()
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT Worker.name
            FROM Worker
            JOIN FilmWorkers ON Worker.worker_id = FilmWorkers.worker_id
            JOIN Film ON FilmWorkers.film_id = Film.film_id
            WHERE Film.name = ? AND FilmWorkers.position = 'actor'
        """, (film_name,))
        actors = cursor.fetchall()
        self.actor_combo_box.addItems([actor[0] for actor in actors])

    def execute_query(self):
        actor_name = self.actor_combo_box.currentText()
        cursor = self.connection.cursor()

        query = """
        WITH ActorCountries AS (
            SELECT DISTINCT FilmCountries.country_id
            FROM FilmCountries
            JOIN FilmWorkers ON FilmCountries.film_id = FilmWorkers.film_id
            JOIN Worker ON FilmWorkers.worker_id = Worker.worker_id
            WHERE Worker.name = ?
        )
        SELECT DISTINCT *
        FROM Worker
        JOIN FilmWorkers ON Worker.worker_id = FilmWorkers.worker_id
        JOIN FilmCountries ON FilmWorkers.film_id = FilmCountries.film_id
        WHERE FilmCountries.country_id IN (SELECT country_id FROM ActorCountries)
        GROUP BY Worker.worker_id
        HAVING COUNT(DISTINCT FilmCountries.country_id) = (SELECT COUNT(*) FROM ActorCountries)
        AND Worker.name != ?
        """

        cursor.execute(query, (actor_name, actor_name))
        rows = cursor.fetchall()

        if rows:
            self.result_table.setRowCount(len(rows))
            self.result_table.setColumnCount(4)
            self.result_table.setHorizontalHeaderLabels(["Worker ID", "Name", "Birth date", "Nationality"])

            for row_idx, row_data in enumerate(rows):
                for col_idx, col_data in enumerate(row_data):
                    self.result_table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        else:
            QMessageBox.information(self, "No results", "No actors found filming in the same countries "
                                                        "as the selected actor.")
