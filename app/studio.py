class Studio:
    def __init__(self, connection):
        self.connection = connection

    def create_studio(self, name):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO Studio (name) VALUES (?)", (name,))
        self.connection.commit()

    def read_studios(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Studio")
        rows = cursor.fetchall()
        return rows

    def update_studio(self, studio_id, name):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE Studio SET name = ? WHERE studio_id = ?", (name, studio_id))
        self.connection.commit()

    def delete_studio(self, studio_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM Studio WHERE studio_id = ?", (studio_id,))
        self.connection.commit()
