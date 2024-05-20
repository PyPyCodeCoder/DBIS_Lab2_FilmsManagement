from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QDateEdit, QMessageBox
from PyQt5.QtCore import QDate


class ComplexQuery3Manager(QWidget):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDisplayFormat("yyyy-MM-dd")
        self.start_date_edit.setDate(QDate.currentDate().addYears(-1))
        self.layout.addWidget(self.start_date_edit)

        self.end_date_edit = QDateEdit()
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDisplayFormat("yyyy-MM-dd")
        self.end_date_edit.setDate(QDate.currentDate())
        self.layout.addWidget(self.end_date_edit)

        self.query_button = QPushButton("Get Actor pairs for a specific period")
        self.query_button.clicked.connect(self.execute_query)
        self.layout.addWidget(self.query_button)

        self.result_table = QTableWidget()
        self.layout.addWidget(self.result_table)

    def execute_query(self):
        start_date = self.start_date_edit.date().toString("yyyy-MM-dd")
        end_date = self.end_date_edit.date().toString("yyyy-MM-dd")

        cursor = self.connection.cursor()
        query = """
        WITH FilmsInPeriod AS (
            SELECT film_id
            FROM Film
            WHERE release_date BETWEEN ? AND ?
        ),
        ActorsInFilms AS (
            SELECT FilmWorkers.film_id, FilmWorkers.worker_id
            FROM FilmWorkers
            WHERE FilmWorkers.film_id IN (SELECT film_id FROM FilmsInPeriod)
        ),
        ActorPairs AS (
            SELECT DISTINCT a1.worker_id AS actor1_id, a2.worker_id AS actor2_id, a1.film_id
            FROM ActorsInFilms a1
            JOIN ActorsInFilms a2 ON a1.film_id = a2.film_id AND a1.worker_id < a2.worker_id
        )
        SELECT w1.name AS actor1, w2.name AS actor2
        FROM ActorPairs ap
        JOIN Worker w1 ON ap.actor1_id = w1.worker_id
        JOIN Worker w2 ON ap.actor2_id = w2.worker_id
        GROUP BY w1.name, w2.name
        HAVING COUNT(DISTINCT ap.film_id) > 0;
        """
        cursor.execute(query, (start_date, end_date))
        rows = cursor.fetchall()

        if rows:
            self.result_table.setRowCount(len(rows))
            self.result_table.setColumnCount(2)
            self.result_table.setHorizontalHeaderLabels(["Actor 1", "Actor 2"])

            for row_idx, row_data in enumerate(rows):
                for col_idx, col_data in enumerate(row_data):
                    self.result_table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        else:
            QMessageBox.information(self, "No results", "No actor pairs found in the specified period.")
