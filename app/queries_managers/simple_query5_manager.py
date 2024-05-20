from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QSpinBox, QMessageBox


class SimpleQuery5Manager(QWidget):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.year_spin_box = QSpinBox()
        self.year_spin_box.setRange(1900, 2100)
        self.year_spin_box.setValue(2000)
        self.layout.addWidget(self.year_spin_box)

        self.query_button = QPushButton("Get Workers involved in Films released after a specified year")
        self.query_button.clicked.connect(self.execute_query)
        self.layout.addWidget(self.query_button)

        self.result_table = QTableWidget()
        self.layout.addWidget(self.result_table)

    def execute_query(self):
        selected_year = self.year_spin_box.value()
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT Worker.*, Film.*
            FROM Worker
            JOIN FilmWorkers ON Worker.worker_id = FilmWorkers.worker_id
            JOIN Film ON FilmWorkers.film_id = Film.film_id
            WHERE Film.release_date > ?
            GROUP BY Worker.worker_id;
        """, (f'{selected_year}-01-01',))
        rows = cursor.fetchall()

        if rows:
            self.result_table.setRowCount(len(rows))
            self.result_table.setColumnCount(4)
            self.result_table.setHorizontalHeaderLabels(["Worker ID", "Name", "Birth date", "Nationality"])

            for row_idx, row_data in enumerate(rows):
                for col_idx, col_data in enumerate(row_data):
                    self.result_table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        else:
            QMessageBox.information(self, "No results",
                                    "No workers found involved in films released after the selected year.")
