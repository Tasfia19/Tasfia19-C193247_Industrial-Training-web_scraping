import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_data_connection():
     
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            passwd=os.getenv("DB_PASS"),
            database=os.getenv("DB_NAME")
        )
        print("MySQL Database connection successful")
        return connection
    except Error as e:
        print(f"The error '{e}' occurred")
        return None

def execute_query(connection, query):
    
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_read_query(connection, query):
   
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")
        return []
    

def create_tables(connection):
       
    create_categories_table = """
    CREATE TABLE IF NOT EXISTS categories (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        description TEXT
    );
    """
    execute_query(connection, create_categories_table)
    
    create_reporters_table = """
    CREATE TABLE IF NOT EXISTS reporters (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL
    );
    """
    execute_query(connection, create_reporters_table)
    
    create_publishers_table = """
    CREATE TABLE IF NOT EXISTS publishers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL
    );
    """
    execute_query(connection, create_publishers_table)
    
    create_news_table = """
    CREATE TABLE IF NOT EXISTS news (
        id INT AUTO_INCREMENT PRIMARY KEY,
        category_id INT,
        reporter_id INT,
        publisher_id INT,
        datetime DATETIME,
        title VARCHAR(255) NOT NULL,
        body TEXT,
        link VARCHAR(255),
        FOREIGN KEY (category_id) REFERENCES categories (id),
        FOREIGN KEY (reporter_id) REFERENCES reporters (id),
        FOREIGN KEY (publisher_id) REFERENCES publishers (id)
    );
    """
    execute_query(connection, create_news_table)
    
    create_images_table = """
    CREATE TABLE IF NOT EXISTS images (
        id INT AUTO_INCREMENT PRIMARY KEY,
        news_id INT,
        image_url VARCHAR(255),
        FOREIGN KEY (news_id) REFERENCES news (id)
    );
    """
    execute_query(connection, create_images_table)
    
    create_summaries_table = """
    CREATE TABLE IF NOT EXISTS summaries (
        id INT AUTO_INCREMENT PRIMARY KEY,
        news_id INT,
        summary_text TEXT,
        FOREIGN KEY (news_id) REFERENCES news (id)
    );
    """
    execute_query(connection, create_summaries_table)

    
if __name__ == "__main__":
    conn = create_data_connection()
    if conn is not None:
        create_tables(conn)