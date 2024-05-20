from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QWidget
from film_worker import FilmWorker
from film import Film
from worker import Worker
from custom_input_dialog import CustomInputDialog


class FilmWorkerManager(QWidget):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.film_worker_manager = FilmWorker(self.connection)
        self.film_manager = Film(self.connection)
        self.worker_manager = Worker(self.connection)

        self.layout = QVBoxLayout()
        self.film_worker_table = QTableWidget()
        self.layout.addWidget(self.film_worker_table)

        self.add_film_worker_button = QPushButton("Add Film Worker")
        self.add_film_worker_button.clicked.connect(self.add_film_worker)
        self.layout.addWidget(self.add_film_worker_button)

        self.delete_film_worker_button = QPushButton("Delete Film Worker")
        self.delete_film_worker_button.clicked.connect(self.delete_film_worker)
        self.layout.addWidget(self.delete_film_worker_button)

        self.setLayout(self.layout)
        self.load_film_workers()

    def load_film_workers(self):
        film_workers = self.film_worker_manager.read_film_workers()
        self.film_worker_table.setRowCount(len(film_workers))
        self.film_worker_table.setColumnCount(4)
        self.film_worker_table.setHorizontalHeaderLabels(["ID", "Film", "Worker", "Position"])

        for row_idx, row_data in enumerate(film_workers):
            for col_idx, col_data in enumerate(row_data):
                self.film_worker_table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

    def add_film_worker(self):
        films = self.film_manager.read_films()
        film_names = [film[1] for film in films]
        film_name, ok = CustomInputDialog.getItem(self, "Add Film Worker", "Select Film:", film_names, 0, False)
        if ok and film_name:
            film_id = [film[0] for film in films if film[1] == film_name][0]

            workers = self.worker_manager.read_workers()
            worker_names = [worker[1] for worker in workers]
            worker_name, ok = CustomInputDialog.getItem(self, "Add Film Worker", "Select Worker:",
                                                        worker_names, 0, False)
            if ok and worker_name:
                worker_id = [worker[0] for worker in workers if worker[1] == worker_name][0]

                position, ok = CustomInputDialog.getText(self, "Add Film Worker", "Position:")
                if ok and position:
                    self.film_worker_manager.create_film_worker(film_id, worker_id, position)
                    self.load_film_workers()

    def delete_film_worker(self):
        selected_items = self.film_worker_table.selectedItems()
        if selected_items:
            film_workers_id = int(selected_items[0].text())
            confirm = QMessageBox.question(self, "Delete Film Worker",
                                           "Are you sure you want to delete this film worker?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if confirm == QMessageBox.Yes:
                self.film_worker_manager.delete_film_worker(film_workers_id)
                self.load_film_workers()
