import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def create_db():
    conn = None
    try:
        password = os.environ.get("DB_PASSWORD")
        conn = psycopg2.connect(
            host="127.0.0.1",
            user="postgres",
            password=password,
            dbname="postgres"
        )
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute("CREATE DATABASE my_arxiv_db")
        print("Database 'my_arxiv_db' create successfully")

    except psycopg2.OperationalError as e:
        print(f"Error: {e}")
    except psycopg2.errors.DuplicateDatabase:
        print("Data base already exists, skipping creation.")

    finally:
        if conn:
            conn.close()



def create_tables():

    password = os.environ.get("DB_PASSWORD")
    conn = psycopg2.connect(
        host="127.0.0.1",
        user="postgres",
        password=password,
        dbname="postgres"
    )
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute("""
                CREATE TABLE IF NOT EXISTS papers 
                    (
                        id SERIAL PRIMARY KEY, 
                        title TEXT, authors TEXT, 
                        summary TEXT, 
                        published TIMESTAMP, 
                        updated TIMESTAMP, 
                        primary_category TEXT, 
                        categories TEXT, 
                        pdf_url TEXT, 
                        arxiv_id TEXT UNIQUE, 
                        doi TEXT, 
                        journal_ref TEXT, 
                        comment TEXT,
                        system_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                   )
                """)
    print("Table 'papers' created successfully")
    conn.close()


if __name__ == "__main__":
    create_db()
    create_tables()




