from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QMessageBox


class SimpleQuery4Manager(QWidget):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.language_combo_box = QComboBox()
        self.populate_languages()
        self.layout.addWidget(self.language_combo_box)

        self.query_button = QPushButton("Get Studios producing Films in a specific language")
        self.query_button.clicked.connect(self.execute_query)
        self.layout.addWidget(self.query_button)

        self.result_table = QTableWidget()
        self.layout.addWidget(self.result_table)

    def populate_languages(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT DISTINCT language FROM Film")
        languages = cursor.fetchall()
        self.language_combo_box.addItems([language[0] for language in languages])

    def execute_query(self):
        selected_language = self.language_combo_box.currentText()
        cursor = self.connection.cursor()
        query = """
            SELECT DISTINCT Studio.studio_id, Studio.name
            FROM Studio
            JOIN Film ON Studio.studio_id = Film.studio_id
            WHERE Film.language = ?
        """
        cursor.execute(query, (selected_language,))
        rows = cursor.fetchall()

        if rows:
            self.result_table.setRowCount(len(rows))
            self.result_table.setColumnCount(2)
            self.result_table.setHorizontalHeaderLabels(["Studio ID", "Name"])

            for row_idx, row_data in enumerate(rows):
                for col_idx, col_data in enumerate(row_data):
                    self.result_table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        else:
            QMessageBox.information(self, "No results", "No studios found producing films in the selected language.")

