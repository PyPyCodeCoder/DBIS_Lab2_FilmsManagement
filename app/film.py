import re
from datetime import datetime
from PyQt5.QtWidgets import QMessageBox


class Film:
    def __init__(self, connection):
        self.connection = connection

    @staticmethod
    def validate_film_details(name, description, release_date, language, duration, budget):
        if release_date:
            if not re.match(r'\d{4}-\d{2}-\d{2}', release_date):
                return False, "Please enter the release date in the format YYYY-MM-DD."

            try:
                datetime.strptime(release_date, '%Y-%m-%d')
            except ValueError:
                return False, "Please enter a valid release date."

        if duration:
            if not re.match(r'^\d{2}:\d{2}:\d{2}$', duration):
                return False, "Please enter the duration in the format HH:MM:SS."

        return True, ""

    def create_film(self, name, description, release_date, language, duration, budget, studio_id, genre_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO Film (name, description, release_date, language, duration, budget, studio_id, genre_id) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (name, description, release_date, language, duration, budget, studio_id, genre_id)
            )
            self.connection.commit()
            return True, "Film added successfully."
        except Exception as e:
            return False, str(e)

    def read_films(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT Film.film_id, Film.name, Film.description, Film.release_date, Film.language, 
            Film.duration, Film.budget, Studio.name as studio_name, Genre.name as genre_name
            FROM Film
            JOIN Studio ON Film.studio_id = Studio.studio_id
            JOIN Genre ON Film.genre_id = Genre.genre_id
        """)
        rows = cursor.fetchall()
        return rows

    def update_film(self, film_id, name, description, release_date, language, duration, budget, studio_id, genre_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "UPDATE Film SET name = ?, description = ?, release_date = ?, language = ?, "
                "duration = ?, budget = ?, studio_id = ?, genre_id = ? WHERE film_id = ?",
                (name, description, release_date, language, duration, budget, studio_id, genre_id, film_id)
            )
            self.connection.commit()
            return True, "Film updated successfully."
        except Exception as e:
            return False, str(e)

    def delete_film(self, film_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM Film WHERE film_id = ?", (film_id,))
            self.connection.commit()
        except Exception as e:
            QMessageBox.warning(None, "Error", str(e))
