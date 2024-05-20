class Country:
    def __init__(self, connection):
        self.connection = connection

    def create_country(self, name):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO Country (name) VALUES (?)", (name,))
        self.connection.commit()

    def read_countries(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Country")
        rows = cursor.fetchall()
        return rows

    def update_country(self, country_id, name):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE Country SET name = ? WHERE country_id = ?", (name, country_id))
        self.connection.commit()

    def delete_country(self, country_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM Country WHERE country_id = ?", (country_id,))
        self.connection.commit()
