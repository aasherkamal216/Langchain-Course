import sqlite3

# connecting to sqlite
conn = sqlite3.connect('student.db')

# cursor
cursor = conn.cursor()

# create the table
table_info = """
CREATE TABLE IF NOT EXISTS STUDENT (
    NAME VARCHAR(30), 
    CLASS VARCHAR(30), 
    SECTION VARCHAR(30),
    MARKS INT
);
"""
# execute the query to create table
cursor.execute(table_info)

# insert data
students_data = [
    ('Alice', 'Data Science', 'A', 85),
    ('Smith', 'DevOps', 'B', 98),
    ('Carol', 'GenAI', 'A', 92),
    ('David', 'DevOps', 'C', 71),
    ('Eva', 'Data Science', 'B', 94),
    ('Frank', 'Machine Learning', 'A', 87),
    ('Grace', 'GenAI', 'C', 81),
    ('Hank', 'GenAI', 'B', 100),
    ('Michael', 'Data Science', 'A', 95),
    ('Jack', 'Machine Learning', 'C', 75)
]

# execute the query to insert data
cursor.executemany("INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES (?, ?, ?, ?);", students_data)

# Print the data
from rich import print
data = cursor.execute("SELECT * FROM STUDENT;")
for row in data:
    print(row)

# commit the changes
conn.commit()

# close the connection
conn.close()
