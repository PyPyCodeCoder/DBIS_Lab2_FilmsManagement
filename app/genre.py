class Genre:
    def __init__(self, connection):
        self.connection = connection

    def create_genre(self, name):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO Genre (name) VALUES (?)", (name,))
        self.connection.commit()

    def read_genres(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Genre")
        rows = cursor.fetchall()
        return rows

    def update_genre(self, genre_id, name):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE Genre SET name = ? WHERE genre_id = ?", (name, genre_id))
        self.connection.commit()

    def delete_genre(self, genre_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM Genre WHERE genre_id = ?", (genre_id,))
        self.connection.commit()
