class FilmWorker:
    def __init__(self, connection):
        self.connection = connection

    def create_film_worker(self, film_id, worker_id, position):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO FilmWorkers (film_id, worker_id, position) VALUES (?, ?, ?)",
                       (film_id, worker_id, position))
        self.connection.commit()

    def read_film_workers(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT FilmWorkers.film_workers_id, Film.name, Worker.name, FilmWorkers.position
            FROM FilmWorkers
            JOIN Film ON FilmWorkers.film_id = Film.film_id
            JOIN Worker ON FilmWorkers.worker_id = Worker.worker_id
        """)
        rows = cursor.fetchall()
        return rows

    def delete_film_worker(self, film_workers_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM FilmWorkers WHERE film_workers_id = ?", (film_workers_id,))
        self.connection.commit()
