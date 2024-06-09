from database.connection import get_db_connection
from models.author import Author

class Magazine:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category
        
        if not isinstance(name, str) or not(2 <= len(name) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters")
        if not isinstance(category ,str) or len(category) == 0:
            raise ValueError("Category must be a non-empty string")
        
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', (name, category))
        conn.commit()
        self._id = c.lastrowid
        conn.close()

    def __repr__(self):
        return f'<Magazine {self.name}>'

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not (2 <= len(value) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters")
        self._name = value
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('UPDATE magazines SET name = ? WHERE id = ?', (value, self._id))
        conn.commit()
        conn.close()
        
        
    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name           
        
        

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Category must be a non-empty string")
        self._category = value
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('UPDATE magazines SET category = ? WHERE id = ?', (value, self._id))
        conn.commit()
        conn.close()

    def articles(self):
        from models.article import Article
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''
            SELECT a.* FROM articles a
            JOIN magazines m ON a.magazine_id = m.id
            WHERE m.id = ?
        ''', (self._id,))
        articles = [Article(row["id"], row["title"], row["content"], row["author_id"], row["magazine_id"]) for row in c.fetchall()]
        conn.close()
        return articles

    def contributors(self):
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''
            SELECT DISTINCT au.* FROM authors au
            JOIN articles a ON a.author_id = au.id
            WHERE a.magazine_id = ?
        ''', (self._id,))
        contributors = [Author(row["id"], row["name"]) for row in c.fetchall()]
        conn.close()
        return contributors

    def article_titles(self):
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''
            SELECT a.title FROM articles a
            JOIN magazines m ON a.magazine_id = m.id
            WHERE m.id = ?
        ''', (self._id,))
        titles = [row["title"] for row in c.fetchall()]
        conn.close()
        return titles if titles else None

    def contributing_authors(self):
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''
            SELECT au.*, COUNT(a.id) as article_count FROM authors au
            JOIN articles a ON a.author_id = au.id
            WHERE a.magazine_id = ?
            GROUP BY au.id
            HAVING article_count > 2
        ''', (self._id,))
        authors = [Author(row["id"], row["name"]) for row in c.fetchall()]
        conn.close()
        return authors if authors else None