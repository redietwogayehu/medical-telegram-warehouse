import psycopg2

conn = psycopg2.connect(
    dbname="medical_warehouse",
    user="betty",
    host="localhost",
    port="5432"
)