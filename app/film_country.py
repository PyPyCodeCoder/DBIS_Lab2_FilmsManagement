class FilmCountry:
    def __init__(self, connection):
        self.connection = connection

    def create_film_country(self, film_id, country_id, description):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO FilmCountries (film_id, country_id, description) VALUES (?, ?, ?)",
                       (film_id, country_id, description))
        self.connection.commit()

    def read_film_countries(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT FilmCountries.film_countries_id, Film.name, Country.name, FilmCountries.description
            FROM FilmCountries
            JOIN Film ON FilmCountries.film_id = Film.film_id
            JOIN Country ON FilmCountries.country_id = Country.country_id
        """)
        rows = cursor.fetchall()
        return rows

    def delete_film_country(self, film_countries_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM FilmCountries WHERE film_countries_id = ?", (film_countries_id,))
        self.connection.commit()
