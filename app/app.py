import sys
import os
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt

from genre_manager import GenreManager
from studio_manager import StudioManager
from worker_manager import WorkerManager
from country_manager import CountryManager
from film_manager import FilmManager
from film_country_manager import FilmCountryManager
from film_worker_manager import FilmWorkerManager

from queries_managers.simple_query1_manager import SimpleQuery1Manager
from queries_managers.simple_query2_manager import SimpleQuery2Manager
from queries_managers.simple_query3_manager import SimpleQuery3Manager
from queries_managers.simple_query4_manager import SimpleQuery4Manager
from queries_managers.simple_query5_manager import SimpleQuery5Manager

from queries_managers.complex_query1_manager import ComplexQuery1Manager
from queries_managers.complex_query2_manager import ComplexQuery2Manager
from queries_managers.complex_query3_manager import ComplexQuery3Manager
from queries_managers.complex_query4_manager import ComplexQuery4Manager
from queries_managers.complex_query5_manager import ComplexQuery5Manager


def create_connection():
    connection = None
    db_path = os.path.join(os.path.dirname(__file__), '..', 'db', 'filmsDB.db')
    try:
        connection = sqlite3.connect(db_path)
        print("Connection to SQLite DB successful")
    except sqlite3.Error as e:
        print(f"The error '{e}' occurred")
    return connection


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Movie database management")
        self.setGeometry(200, 200, 1600, 600)

        self.connection = create_connection()

        main_layout = QHBoxLayout()

        self.menu = QWidget()
        self.menu_layout = QVBoxLayout()

        label = QLabel("CRUD for database tables:")
        label.setAlignment(Qt.AlignCenter)
        self.menu_layout.addWidget(label)

        self.add_menu_button("Manage Films", self.manage_films)
        self.add_menu_button("Manage Workers", self.manage_workers)
        self.add_menu_button("Manage Countries", self.manage_countries)
        self.add_menu_button("Manage Studios", self.manage_studios)
        self.add_menu_button("Manage Genres", self.manage_genres)
        self.add_menu_button("Manage Film Countries", self.manage_film_countries)
        self.add_menu_button("Manage Film Workers", self.manage_film_workers)

        label = QLabel("Simple queries:")
        label.setAlignment(Qt.AlignCenter)
        self.menu_layout.addWidget(label)

        self.add_menu_button("Films from a specific Studio", self.simple_query1)
        self.add_menu_button("Films of a specific Genre", self.simple_query2)
        self.add_menu_button("Countries where a specific Studio worked", self.simple_query3)
        self.add_menu_button("Studios producing Films in a specific language", self.simple_query4)
        self.add_menu_button("Workers involved in Films released after a specified year", self.simple_query5)

        label = QLabel("Complex queries:")
        label.setAlignment(Qt.AlignCenter)
        self.menu_layout.addWidget(label)

        self.add_menu_button("Find Actors filming in same Countries", self.complex_query1)
        self.add_menu_button("Find Studios filming in all Genres", self.complex_query2)
        self.add_menu_button("Get Actor pairs for a specific period", self.complex_query3)

        label = QLabel("Queries suggested by teacher:")
        label.setAlignment(Qt.AlignCenter)
        self.menu_layout.addWidget(label)

        self.add_menu_button("Find Actors who acted in all Films of a specific Actor and more", self.complex_query4)
        self.add_menu_button("Find Actors with exact Film match", self.complex_query5)

        self.menu.setLayout(self.menu_layout)

        self.main_content = QWidget()
        self.main_content_layout = QVBoxLayout()
        self.main_content.setLayout(self.main_content_layout)
        label = QLabel("Choose an option from the menu")
        label.setAlignment(Qt.AlignCenter)
        self.main_content_layout.addWidget(label)

        main_layout.addWidget(self.menu)
        main_layout.addWidget(self.main_content, 1)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def add_menu_button(self, name, method):
        button = QPushButton(name)
        button.clicked.connect(method)
        self.menu_layout.addWidget(button)

    def manage_films(self):
        self.clear_layout(self.main_content_layout)
        film_manager_widget = FilmManager(self.connection)
        self.main_content_layout.addWidget(film_manager_widget)

    def manage_workers(self):
        self.clear_layout(self.main_content_layout)
        worker_manager_widget = WorkerManager(self.connection)
        self.main_content_layout.addWidget(worker_manager_widget)

    def manage_countries(self):
        self.clear_layout(self.main_content_layout)
        country_manager_widget = CountryManager(self.connection)
        self.main_content_layout.addWidget(country_manager_widget)

    def manage_studios(self):
        self.clear_layout(self.main_content_layout)
        studio_manager_widget = StudioManager(self.connection)
        self.main_content_layout.addWidget(studio_manager_widget)

    def manage_genres(self):
        self.clear_layout(self.main_content_layout)
        genre_manager_widget = GenreManager(self.connection)
        self.main_content_layout.addWidget(genre_manager_widget)

    def manage_film_countries(self):
        self.clear_layout(self.main_content_layout)
        film_country_manager_widget = FilmCountryManager(self.connection)
        self.main_content_layout.addWidget(film_country_manager_widget)

    def manage_film_workers(self):
        self.clear_layout(self.main_content_layout)
        film_worker_manager_widget = FilmWorkerManager(self.connection)
        self.main_content_layout.addWidget(film_worker_manager_widget)

    def simple_query1(self):
        self.clear_layout(self.main_content_layout)
        simple_query1_manager_widget = SimpleQuery1Manager(self.connection)
        self.main_content_layout.addWidget(simple_query1_manager_widget)

    def simple_query2(self):
        self.clear_layout(self.main_content_layout)
        simple_query2_manager_widget = SimpleQuery2Manager(self.connection)
        self.main_content_layout.addWidget(simple_query2_manager_widget)

    def simple_query3(self):
        self.clear_layout(self.main_content_layout)
        simple_query3_manager_widget = SimpleQuery3Manager(self.connection)
        self.main_content_layout.addWidget(simple_query3_manager_widget)

    def simple_query4(self):
        self.clear_layout(self.main_content_layout)
        simple_query4_manager_widget = SimpleQuery4Manager(self.connection)
        self.main_content_layout.addWidget(simple_query4_manager_widget)

    def simple_query5(self):
        self.clear_layout(self.main_content_layout)
        simple_query5_manager_widget = SimpleQuery5Manager(self.connection)
        self.main_content_layout.addWidget(simple_query5_manager_widget)

    def complex_query1(self):
        self.clear_layout(self.main_content_layout)
        complex_query1_widget = ComplexQuery1Manager(self.connection)
        self.main_content_layout.addWidget(complex_query1_widget)

    def complex_query2(self):
        self.clear_layout(self.main_content_layout)
        complex_query2_widget = ComplexQuery2Manager(self.connection)
        self.main_content_layout.addWidget(complex_query2_widget)

    def complex_query3(self):
        self.clear_layout(self.main_content_layout)
        complex_query3_widget = ComplexQuery3Manager(self.connection)
        self.main_content_layout.addWidget(complex_query3_widget)

    def complex_query4(self):
        self.clear_layout(self.main_content_layout)
        complex_query4_widget = ComplexQuery4Manager(self.connection)
        self.main_content_layout.addWidget(complex_query4_widget)

    def complex_query5(self):
        self.clear_layout(self.main_content_layout)
        complex_query5_widget = ComplexQuery5Manager(self.connection)
        self.main_content_layout.addWidget(complex_query5_widget)

    @staticmethod
    def clear_layout(layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.clear_layout(self.main_content_layout)

            label = QLabel("Choose an option from the menu")
            label.setAlignment(Qt.AlignCenter)
            self.main_content_layout.addWidget(label)
        else:
            super().keyPressEvent(event)

    def closeEvent(self, event):
        if self.connection:
            self.connection.close()
            print("Connection to SQLite DB closed")
        event.accept()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
