import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    
    def __init__(self, name, breed, id=None):
        self.name = name
        self.breed = breed
        self.id = id

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs
                (id INTEGER PRIMARY KEY, 
                name TEXT,
                breed TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS dogs 
        """    
        CURSOR.execute(sql)
        CONN.commit()


    def save(self):
        sql = """
            INSERT INTO dogs (name, breed)
            VALUES (?, ?)
        """

        CURSOR.execute(sql,(self.name, self.breed))
        CONN.commit()
        self.id = CURSOR.lastrowid

    @classmethod
    def create(cls, name, breed):
        new_dog = cls(name, breed)
        new_dog.save()
        return new_dog
    
    @classmethod
    def new_from_db(cls, row):
        new_dog = cls(
            name=row[1],
            breed=row[2],
            id=row[0]
        )

        return new_dog

    @classmethod
    def get_all(cls):
        sql = """
            SELECT * FROM dogs
        """

        results = CURSOR.execute(sql).fetchall()
        return [cls.new_from_db(row) for row in results]
    
    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT * FROM dogs
            WHERE name = ?
            LIMIT 1
        """

        match = CURSOR.execute(sql, (name,)).fetchone()
        if not match:
            return None

        return Dog(
            name=match[1],
            breed=match[2],
            id=match[0]
        )
    


    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * FROM dogs
            WHERE id = ?
            LIMIT 1
        """

        found = CURSOR.execute(sql, (id,)).fetchone()
        if not found:
            return None

        return Dog(
            name=found[1],
            breed=found[2],
            id=found[0]
        )

    @classmethod
    def find_or_create_by(cls, name=None, breed=None):
        sql = """
            SELECT * FROM dogs
            WHERE (name, breed) = (?, ?)
            LIMIT 1
        """

        found = CURSOR.execute(sql, (name, breed)).fetchone()
        if not found:
            sql = """
                INSERT INTO dogs (name, breed)
                VALUES (?, ?)
            """

            CURSOR.execute(sql, (name, breed))
            return Dog(
                name=name,
                breed=breed,
                id=CURSOR.lastrowid
            )

        return Dog(
            name=found[1],
            breed=found[2],
            id=found[0]
        )

    def update(self):
        sql = """
            UPDATE dogs
            SET name = ?,
                breed = ?
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.name, self.breed, self.id))
        CONN.commit()