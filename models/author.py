from database.connection import get_db_connection


class Author:
    def __init__(self, id = None, name = None):
        self.id = id
        self.name = name
        
        if name is not None and (not isinstance(name, str) or len(name) == 0):
            raise ValueError("Name must be a non-empty string")
        if name is not None and id is None:
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("INSERT INTO authors (name) VALUES (?)", (name,))
            conn.commit()
            self._id = c.lastrowid
            conn.close()

    def __repr__(self):
        return f'<Author {self.name}>'
    
        
    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        raise AttributeError("Name attribute is read-only")

    def articles(self):
        from models.article import Article
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''
            SELECT a.* FROM articles a
            JOIN authors au ON a.author_id = au.id
            WHERE au.id = ?
        ''', (self._id,))
        articles = [Article(row["id"], row["title"], row["content"], row["author_id"], row["magazine_id"]) for row in c.fetchall()]
        conn.close()
        return articles

    def magazines(self):
        from models.magazine import Magazine
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''
            SELECT DISTINCT m.* FROM magazines m
            JOIN articles a ON a.magazine_id = m.id
            WHERE a.author_id = ?
        ''', (self._id,))
        magazines = [Magazine(row["id"], row["name"], row["category"]) for row in c.fetchall()]
        conn.close()
        return magazines