import psycopg2


def get_connection():
    return psycopg2.connect(
        dbname="medical_warehouse",
        user="betty",
        host="localhost",
        port="5432"
    )