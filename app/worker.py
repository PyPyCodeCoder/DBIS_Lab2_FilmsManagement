class Worker:
    def __init__(self, connection):
        self.connection = connection

    def create_worker(self, name, birth_date, nationality):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO Worker (name, birth_date, nationality) VALUES (?, ?, ?)",
                       (name, birth_date, nationality))
        self.connection.commit()

    def read_workers(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Worker")
        rows = cursor.fetchall()
        return rows

    def update_worker(self, worker_id, name, birth_date, nationality):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE Worker SET name = ?, birth_date = ?, nationality = ? WHERE worker_id = ?",
                       (name, birth_date, nationality, worker_id))
        self.connection.commit()

    def delete_worker(self, worker_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM Worker WHERE worker_id = ?", (worker_id,))
        self.connection.commit()
