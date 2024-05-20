from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox


class ComplexQuery2Manager(QWidget):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.query_button = QPushButton("Find Studios filming in all Genres")
        self.query_button.clicked.connect(self.execute_query)
        self.layout.addWidget(self.query_button)

        self.result_table = QTableWidget()
        self.layout.addWidget(self.result_table)

    def execute_query(self):
        cursor = self.connection.cursor()

        query = """
        SELECT Studio.studio_id, Studio.name
        FROM Studio
        JOIN Film ON Studio.studio_id = Film.studio_id
        JOIN Genre ON Film.genre_id = Genre.genre_id
        GROUP BY Studio.studio_id
        HAVING COUNT(DISTINCT Genre.genre_id) = (SELECT COUNT(DISTINCT genre_id) FROM Genre)
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        if rows:
            self.result_table.setRowCount(len(rows))
            self.result_table.setColumnCount(2)
            self.result_table.setHorizontalHeaderLabels(["Studio ID", "Name"])

            for row_idx, row_data in enumerate(rows):
                for col_idx, col_data in enumerate(row_data):
                    self.result_table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        else:
            QMessageBox.information(self, "No results", "No studios found filming in all genres.")
