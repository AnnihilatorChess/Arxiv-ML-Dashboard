import psycopg2


def create_db():
    conn = None
    try:
        conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="<password>",
            dbname="postgres"
        )
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute("CREATE DATABASE my_arxiv_db")
        print("Database 'my_arxiv_db' create successfully")

    except psycopg2.OperationalError as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    create_db()

