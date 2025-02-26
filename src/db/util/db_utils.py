# TODO Make db path more robust
# TODO Fix indentation
import sqlite3
from sqlite3 import Error

def get_connection(db_path: str) -> sqlite3.Connection:
    """
    Create and return a new database connection.
    
    :param db_path: Path to the SQLite database file.
    :return: sqlite3.Connection object.
    """
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        raise

def query_db(db_path: str, query: str, params: tuple = ()) -> list:
    """
    Execute a SELECT query and return all fetched rows.
    
    :param db_path: Path to the SQLite database file.
    :param query: SQL query to execute.
    :param params: Optional tuple of parameters to use with the query.
    :return: List of rows returned by the query.
    """
    conn = get_connection(db_path)
    try:
        cur = conn.cursor()
        cur.execute(query, params)
        rows = cur.fetchall()
        return rows
    except Error as e:
        print(f"Error executing query: {e}")
        raise
    finally:
        conn.close()

def insert_db(db_path: str, query: str, params: tuple) -> int:
    """
    Execute an INSERT (or other data-changing) statement.
    
    :param db_path: Path to the SQLite database file.
    :param query: SQL statement to execute.
    :param params: Tuple of parameters to use with the statement.
    :return: The last row ID of the inserted row.
    """
    conn = get_connection(db_path)
    try:
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        return cur.lastrowid
    except Error as e:
        print(f"Error executing insert: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == '__main__':
    db_file = '../main.db'
    
    # Example: Insert a Lesson
    insert_query = "INSERT INTO lessons (name, description) VALUES (?, ?)"
    lesson_data = ("Multiplication Facts", "PRACTICE YOUR FACTS!")
    lesson_id = insert_db(db_file, insert_query, lesson_data)
    print(f"Inserted Lesson with ID: {lesson_id}")

    # Example: Query users
    select_query = "SELECT id, name, description FROM lessons"
    lessons = query_db(db_file, select_query)
    print("Lessons in database:")
    for lesson in lessons:
        print(lesson)