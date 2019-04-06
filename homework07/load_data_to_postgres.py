import psycopg2
import csv

conn = psycopg2.connect("host=127.0.0.1 port=5432 dbname=adult_data user=postgres password=z12x34c43v21")
cursor = conn.cursor()

query = """
CREATE TABLE IF NOT EXISTS adult_data (
    id SERIAL PRIMARY KEY,
    age INTEGER,
    workclass VARCHAR,
    fnlwgt INTEGER,
    education VARCHAR,
    education_num INTEGER,
    marital_status VARCHAR,
    occupation VARCHAR,
    relationship VARCHAR,
    race VARCHAR,
    sex VARCHAR,
    capital_gain INTEGER,
    capital_loss INTEGER,
    hours_per_week INTEGER,
    native_country VARCHAR,
    salary VARCHAR
)
"""

cursor.execute(query)
conn.commit()

with open('adultdata.csv', 'r') as f:
    reader = csv.reader(f)
    # Skip the header row
    next(reader)
    for Id, row in enumerate(reader):
        cursor.execute(
            "INSERT INTO adult_data VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            [Id] + row
        )
conn.commit()

