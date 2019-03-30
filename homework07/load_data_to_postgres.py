import psycopg2
import csv

conn = psycopg2.connect("host=localhost port=5433 dbname=odscourse user=postgres password=secret")
cursor = conn.cursor()

query = """
CREATE TABLE IF NOT EXISTS adult_data (
    id SERIAL PRIMARY KEY,
    age INTEGER,
    workclass VARCHAR,
    fnlwgt INTEGER,
    education VARCHAR,
    education-num INTEGER,
    marital-status VARCHAR,
    occupation VARCHAR,
    relationship VARCHAR,
    race VARCHAR,
    sex VARCHAR,
    capital-gain INTEGER,
    capital-loss INTEGER,
    hours-per-week INTEGER,
    native-country VARCHAR,
    salary VARCHAR
)
"""

cursor.execute(query)
conn.commit()

with open('adult_data.csv', 'r') as f:
    reader = csv.reader(f)
    # Skip the header row
    next(reader)
    for Id, row in enumerate(reader):
        cursor.execute(
            "INSERT INTO adult_data VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            [Id] + row
        )
conn.commit()
