sql_create_coach_table = """
    CREATE TABLE IF NOT EXISTS coach (
        id INTEGER PRIMARY KEY NOT NULL UNIQUE,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        gender char(1) NOT NULL CHECK (gender IN ('M', 'F')),
        phone_number CHAR(10) NOT NULL
    );"""

sql_create_athlete_table = """
    CREATE TABLE IF NOT EXISTS athlete (
        id INTEGER PRIMARY KEY NOT NULL UNIQUE,
        coach_id INTEGER NOT NULL,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        gender NOT NULL CHECK (gender IN ('M', 'F')),
        phone_number CHAR(10) NOT NULL,
        FOREIGN KEY (coach_id) REFERENCES coach (id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    );"""

sql_create_training_plan_table = """
    CREATE TABLE IF NOT EXISTS training_plan (
        id INTEGER PRIMARY KEY NOT NULL UNIQUE,
        coach_id INTEGER NOT NULL,
        athlete_id INTEGER NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE NOT NULL,
        event VARCHAR(50) NOT NULL,
        FOREIGN KEY (coach_id) REFERENCES coach (id)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
        FOREIGN KEY (athlete_id) REFERENCES athlete (id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    );"""

sql_create_workout_table = """
    CREATE TABLE IF NOT EXISTS workout (
        id INTEGER PRIMARY KEY NOT NULL UNIQUE,
        athlete_id INTEGER NOT NULL,
        training_plan_id INTEGER NOT NULL,
        date DATE NOT NULL,
        duration INTEGER NOT NULL,
        type NOT NULL CHECK (type IN ('run', 'cross-train')) ,
        coach_notes VARCHAR(255),
        athlete_notes VARCHAR(255),
        FOREIGN KEY (athlete_id) REFERENCES athlete (id)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
        FOREIGN KEY (training_plan_id) REFERENCES training_plan (id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    );"""

sql_create_metrics_table = """
    CREATE TABLE IF NOT EXISTS metrics (
        id INTEGER PRIMARY KEY NOT NULL UNIQUE,
        athlete_id INTEGER NOT NULL,
        date DATE NOT NULL,
        resting_heart_rate INTEGER,
        hrv_value INTEGER,
        hrv_status CHECK (hrv_status IN ('low', 'balanced', 'high')),
        sleep_score INTEGER CHECK (sleep_score >= 0 AND sleep_score <= 100),
        FOREIGN KEY (athlete_id) REFERENCES athlete (id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    );"""

def get_schema():
    schema = f"{sql_create_coach_table} {sql_create_athlete_table} {sql_create_training_plan_table} {sql_create_workout_table} {sql_create_metrics_table}"
    return schema