from database.setup import create_tables
from database.connection import get_db_connection
from models.article import Article
from models.author import Author
from models.magazine import Magazine

def main():
    try:
        
        author = Author("Jane Doe")
        print(f"Author created with ID: {author.id}, Name: {author.name}")

        
        magazine = Magazine("Science Today", "Science")
        print(f"Magazine created with ID: {magazine.id}, Name: {magazine.name}, Category: {magazine.category}")

       
        article = Article(author, magazine, "Exploring Quantum Physics", "This is a detailed article about quantum physics.")
        print(f"Article created with ID: {article.id}, Title: {article.title}, Content: {article.content}")

      
        print(f"Article Author: {article.author.name}")
        print(f"Article Magazine: {article.magazine.name}")

       
       
        author_articles = author.articles()
        print(f"Articles by Author: {[article.title for article in author_articles]}")
        
        author_magazines = author.magazines()
        print(f"Magazines by Author: {[magazine.name for magazine in author_magazines]}")

        # Test Magazine methods
        magazine_articles = magazine.articles()
        print(f"Articles in Magazine: {[article.title for article in magazine_articles]}")
        
        magazine_contributors = magazine.contributors()
        print(f"Contributors to Magazine: {[contributor.name for contributor in magazine_contributors]}")

        magazine_article_titles = magazine.article_titles()
        print(f"Article Titles in Magazine: {magazine_article_titles}")

        magazine_contributing_authors = magazine.contributing_authors()
        print(f"Contributing Authors to Magazine: {[author.name for author in magazine_contributing_authors]}")

    except Exception as e:
        print(f"Error: {e}")

    # Initialize the database and create tables
    create_tables()

    # Collect user input
    author_name = input("Enter author's name: ")
    magazine_name = input("Enter magazine name: ")
    magazine_category = input("Enter magazine category: ")
    article_title = input("Enter article title: ")
    article_content = input("Enter article content: ")

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()


    '''
        The following is just for testing purposes, 
        you can modify it to meet the requirements of your implmentation.
    '''

    # Create an author
    cursor.execute('INSERT INTO authors (name) VALUES (?)', (author_name,))
    author_id = cursor.lastrowid # Use this to fetch the id of the newly created author

    # Create a magazine
    cursor.execute('INSERT INTO magazines (name, category) VALUES (?,?)', (magazine_name, magazine_category))
    magazine_id = cursor.lastrowid # Use this to fetch the id of the newly created magazine

    # Create an article
    cursor.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)',
                   (article_title, article_content, author_id, magazine_id))

    conn.commit()

    # Query the database for inserted records. 
    # The following fetch functionality should probably be in their respective models

    cursor.execute('SELECT * FROM magazines')
    magazines = cursor.fetchall()

    cursor.execute('SELECT * FROM authors')
    authors = cursor.fetchall()

    cursor.execute('SELECT * FROM articles')
    articles = cursor.fetchall()

    conn.close()

    # Display results
    print("\nMagazines:")
    for magazine in magazines:
        print(Magazine(magazine["id"], magazine["name"], magazine["category"]))

    print("\nAuthors:")
    for author in authors:
        print(Author(author["id"], author["name"]))

    print("\nArticles:")
    for article in articles:
        print(Article(article["id"], article["title"], article["content"], article["author_id"], article["magazine_id"]))

if __name__ == "__main__":
    main()
