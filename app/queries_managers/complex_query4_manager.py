from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QMessageBox
from PyQt5.QtCore import Qt


class ComplexQuery4Manager(QWidget):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.actor_combo_box = QComboBox()
        self.populate_actors()
        self.layout.addWidget(self.actor_combo_box)

        self.query_button = QPushButton("Find Actors who acted in all Films of a specific Actor and more")
        self.query_button.clicked.connect(self.execute_query)
        self.layout.addWidget(self.query_button)

        self.result_table = QTableWidget()
        self.layout.addWidget(self.result_table)

    def populate_actors(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM Worker")
        actors = cursor.fetchall()
        self.actor_combo_box.addItems([actor[0] for actor in actors])

    def execute_query(self):
        selected_actor = self.actor_combo_box.currentText()
        cursor = self.connection.cursor()

        query = """
        SELECT DISTINCT Worker.name
        FROM Worker
        WHERE NOT EXISTS (
            SELECT worker_id
            FROM FilmWorkers
            WHERE FilmWorkers.worker_id IN (
                SELECT Worker.worker_id
                FROM Worker
                JOIN FilmWorkers ON Worker.worker_id = FilmWorkers.worker_id
                WHERE Worker.name = ?
            )
            AND FilmWorkers.film_id NOT IN (
                SELECT FilmWorkers.film_id
                FROM FilmWorkers
                WHERE FilmWorkers.worker_id = Worker.worker_id
            )
        )
        AND EXISTS (
            SELECT worker_id
            FROM FilmWorkers
            WHERE FilmWorkers.worker_id = Worker.worker_id 
            AND FilmWorkers.film_id NOT IN (
                SELECT FilmWorkers.film_id
                FROM FilmWorkers
                WHERE FilmWorkers.worker_id IN (
                    SELECT Worker.worker_id
                    FROM Worker
                    JOIN FilmWorkers ON Worker.worker_id = FilmWorkers.worker_id
                    WHERE Worker.name = ?
                )
            )
        )
        """

        cursor.execute(query, (selected_actor, selected_actor,))
        rows = cursor.fetchall()

        if rows:
            self.result_table.setRowCount(len(rows))
            self.result_table.setColumnCount(1)
            self.result_table.setHorizontalHeaderLabels(["Actor Name"])

            for row_idx, row_data in enumerate(rows):
                self.result_table.setItem(row_idx, 0, QTableWidgetItem(row_data[0]))
        else:
            QMessageBox.information(self, "No results", "No actors found who acted in all films of the selected actor and more.")
