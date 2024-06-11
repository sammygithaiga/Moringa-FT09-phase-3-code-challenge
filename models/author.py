from database.connection import get_db_connection

class Author:
    def __init__(self, id=None, name=None):
        if name is not None and (not isinstance(name, str) or len(name) == 0):
            raise ValueError("Name must be a non-empty string")

        self._id = id
        self._name = name

        
        if name is not None:
            conn = get_db_connection()
            c = conn.cursor()
            c.execute('INSERT INTO authors (name) VALUES (?)', (name,))
            conn.commit()
            self._id = c.lastrowid
            conn.close()



    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        raise AttributeError("Name attribute is read-only")
