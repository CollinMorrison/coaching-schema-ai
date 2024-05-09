import os
from db import create_table, create_connection
from schema import *

def insert_into_coach(conn):
    sql = """
        INSERT INTO coach (id, first_name, last_name, gender, phone_number) VALUES
            (1, 'John', 'Doe', 'M', '1234567890'),
            (2, 'Jane', 'Smith', 'F', '9876543210'),
            (3, 'Alex', 'Johnson', 'M', '5551234567');
    """

    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return cur.lastrowid

def insert_into_athlete(conn):
    sql = """
        INSERT INTO athlete (coach_id, first_name, last_name, gender, phone_number) VALUES
            (1, 'Michael', 'Johnson', 'M', '1234567890'),
            (2, 'Emily', 'Smith', 'F', '9876543210'),
            (3, 'Chris', 'Taylor', 'M', '5551234567');
    """

    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return cur.lastrowid

def insert_into_training_plan(conn):
    sql = """
        INSERT INTO training_plan (coach_id, athlete_id, start_date, end_date, event) VALUES
            (1, 1, '2024-05-01', '2024-05-31', 'Marathon Preparation'),
            (2, 2, '2024-06-01', '2024-06-30', 'Sprint Training'),
            (3, 3, '2024-07-01', '2024-07-31', 'Triathlon Training');
    """

    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return cur.lastrowid

def insert_into_workout(conn):
    sql = """
        INSERT INTO workout (athlete_id, training_plan_id, date, duration, type, coach_notes, athlete_notes) VALUES
            (1, 1, '2024-05-05', 60, 'run', 'Keep a steady pace', 'Felt great today!'),
            (2, 2, '2024-06-10', 45, 'cross-train', 'Focus on form', 'Feeling a bit tired'),
            (3, 3, '2024-07-15', 75, 'run', 'Push yourself', 'Need to hydrate better next time');
    """

    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return cur.lastrowid

def insert_into_metrics(conn):
    sql = """
        INSERT INTO metrics (athlete_id, date, resting_heart_rate, hrv_value, hrv_status, sleep_score) VALUES
            (1, '2024-05-01', 60, 70, 'balanced', 85),
            (2, '2024-06-01', 65, 75, 'high', 92),
            (3, '2024-07-01', 58, 72, 'low', 78);
    """

    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return cur.lastrowid

def main():
    database = "./database.db"

    conn = create_connection(database)
    create_table(conn, sql_create_coach_table)
    insert_into_coach(conn)
    create_table(conn, sql_create_athlete_table)
    insert_into_athlete(conn)
    create_table(conn, sql_create_training_plan_table)
    insert_into_training_plan(conn)
    create_table(conn, sql_create_workout_table)
    insert_into_workout(conn)
    create_table(conn, sql_create_metrics_table)
    insert_into_metrics(conn)

    print("Database setup complete")

if __name__ == '__main__':
    main()
