from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QMessageBox


class ComplexQuery5Manager(QWidget):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.actor_combo_box = QComboBox()
        self.populate_actors()
        self.layout.addWidget(self.actor_combo_box)

        self.query_button = QPushButton("Find Actors with exact Film match")
        self.query_button.clicked.connect(self.execute_query)
        self.layout.addWidget(self.query_button)

        self.result_table = QTableWidget()
        self.layout.addWidget(self.result_table)

    def populate_actors(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT DISTINCT name FROM Worker")
        actors = cursor.fetchall()
        self.actor_combo_box.addItems([actor[0] for actor in actors])

    def execute_query(self):
        selected_actor = self.actor_combo_box.currentText()
        cursor = self.connection.cursor()

        query = """
        SELECT DISTINCT Worker.name
        FROM Worker
        JOIN FilmWorkers ON Worker.worker_id = FilmWorkers.worker_id
        WHERE NOT EXISTS (
            SELECT FilmWorkers.worker_id
            FROM FilmWorkers AS FW1
            JOIN Worker AS W1 ON FW1.worker_id = W1.worker_id
            WHERE W1.name = ?
            AND NOT EXISTS (
                SELECT FW2.worker_id
                FROM FilmWorkers AS FW2
                WHERE FW2.worker_id = Worker.worker_id
                AND FW2.film_id = FW1.film_id
            )
        )
        AND NOT EXISTS (
            SELECT FilmWorkers.worker_id
            FROM FilmWorkers AS FW3
            WHERE FW3.worker_id = Worker.worker_id
            AND NOT EXISTS (
                SELECT FW4.worker_id
                FROM FilmWorkers AS FW4
                JOIN Worker AS W2 ON FW4.worker_id = W2.worker_id
                WHERE W2.name = ?
                AND FW4.film_id = FW3.film_id
            )
        )
        AND Worker.name != ?
        """

        cursor.execute(query, (selected_actor, selected_actor, selected_actor,))
        rows = cursor.fetchall()

        if rows:
            self.result_table.setRowCount(len(rows))
            self.result_table.setColumnCount(1)
            self.result_table.setHorizontalHeaderLabels(["Actor Name"])

            for row_idx, row_data in enumerate(rows):
                self.result_table.setItem(row_idx, 0, QTableWidgetItem(row_data[0]))
        else:
            QMessageBox.information(self, "No results", "No actors found with an exact film match to the selected actor.")
