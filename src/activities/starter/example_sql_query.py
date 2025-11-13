import sqlite3
from pathlib import Path


def sample_select_queries(db_path):
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    # Select all rows and columns from the student table
    cur.execute('SELECT * FROM student')
    rows = cur.fetchall()  # Fetches more than 1 row
    print("\nAll rows and columns from the student table\n")
    for row in rows:
        print(row)

    # Select the student_id column
    cur.execute('SELECT student_id FROM student WHERE student_name="Alice Brown"')
    row = cur.fetchone()  # Fetches the first result
    print("\nSelect the student_id: \n", row[0])

    cur.execute('SELECT teacher_name, teacher_email FROM teacher WHERE teacher_id in (1, 2)')
    rows = cur.fetchall()  # Fetches all rows from the result
    print("\nTeacher name and email where the teacher is id 1 or 2\n")
    for row in rows:
        print(row)

    con.close()


def main():
    db_path = resources.files(data).joinpath("sample.db")
def main():
    # locate the sample.db file relative to this script: go up to the activities package and into the data folder
    db_path = Path(__file__).resolve().parents[1].joinpath("data", "sample.db")
    sample_select_queries(str(db_path))


if __name__ == "__main__":
    main()
