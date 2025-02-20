import sqlite3
from pathlib import Path
import os

# If this file location changes, this will break.
DB_DIR = Path(__file__).parent

db_file = os.path.join(DB_DIR, "main.db")

sql_statements = [
  """CREATE TABLE IF NOT EXISTS lessons (
    id INTEGER PRIMARY KEY,
    name text NOT NULL, 
    description text
  )
  """,

  """CREATE TABLE IF NOT EXISTS flashcards (
    lesson_id INT NOT NULL,
    challenge text NOT NULL,
    answer text NOT NULL,
    FOREIGN KEY (lesson_id) REFERENCES lessons (id) ON DELETE CASCADE
  )
  """
]

tables = ("lessons", "flashcards")

try:
  with sqlite3.connect(db_file) as conn:
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS lessons")
    cursor.execute("DROP TABLE IF EXISTS flashcards")

    conn.commit()

    for statement in sql_statements:
      cursor.execute(statement)

    conn.commit()

    print("Tables created.")

except sqlite3.OperationalError as e:
  print("Table creation failed: ", e)
