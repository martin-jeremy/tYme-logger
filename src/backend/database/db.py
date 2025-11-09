import os

import duckdb
from pathlib import Path

DB_PATH = Path.home() / ".local" / "tyme-logger" / "tyme.db"


def init_db():
    """Initialize database and schema if needed."""
    # Ensure directory exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Connect to database (creates it if doesn't exist)
    conn = duckdb.connect(str(DB_PATH))

    # Check if tables already exist
    existing_tables = conn.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_schema='main'"
    ).fetchall()
    existing_table_names = {row[0] for row in existing_tables}

    # Only create schema if tables don't exist
    if not existing_table_names:
        print(f"Creating schema in {DB_PATH}")

        # Create sequences first
        conn.execute("CREATE SEQUENCE seq_activity_id START 1")
        conn.execute("CREATE SEQUENCE seq_project_id START 1")
        conn.execute("CREATE SEQUENCE seq_sprint_id START 1")
        conn.execute("CREATE SEQUENCE seq_task_id START 1")
        conn.execute("CREATE SEQUENCE seq_log_id START 1")

        # Activities table
        conn.execute("""
                     CREATE TABLE Activities
                     (
                         id             INTEGER PRIMARY KEY DEFAULT nextval('seq_activity_id'),
                         value          VARCHAR NOT NULL UNIQUE
                     )
                     """)
        conn.execute("""
                     INSERT INTO Activities (value) VALUES 
                         ('Déploiement'),
                         ('Design'),
                         ('Développement'),
                         ('Documentation'),
                         ('Etude'),
                         ('Exigence'),
                         ('Suivi de projet'),
                         ('Test en cours'),
                         ('Transverse')
                     """)

        # Projects table
        conn.execute("""
                     CREATE TABLE Projects
                     (
                         id    INTEGER PRIMARY KEY DEFAULT nextval('seq_project_id'),
                         value VARCHAR NOT NULL UNIQUE
                     )
                     """)
        conn.execute("""
                     INSERT INTO Projects (value)
                     VALUES ('Lab Composer (corelab)'),
                            ('Lab Composer - ProteinHub (TBS)'),
                            ('Lab Composer - TDMind (TechniData)'),
                            ('Lab Composer - ResultManager (Quidel Ortho)'),
                            ('EVM'),
                            ('Infection Tracker'),
                            ('sthemE - v1'),
                            ('sthemE - v2'),
                            ('DMV'),
                            ('Ylink'),
                            ('Outil interne')
                     """)

        # Sprint table
        conn.execute("""
                     CREATE TABLE Sprints
                     (
                         id            INTEGER PRIMARY KEY DEFAULT nextval('seq_sprint_id'),
                         tfs_number    VARCHAR NOT NULL UNIQUE,
                         code          VARCHAR NOT NULL,
                         starting_date DATE    NOT NULL,
                         ending_date   DATE    NOT NULL
                     )
                     """)

        # Task table
        conn.execute("""
                     CREATE TABLE Tasks
                     (
                         id             INTEGER PRIMARY KEY DEFAULT nextval('seq_task_id'),
                         tfs_number     VARCHAR NOT NULL,
                         description    VARCHAR NOT NULL, 
                         sprint_id      INTEGER NOT NULL,
                         project_id     INTEGER,
                         activity_id    INTEGER,
                         status         VARCHAR NOT NULL,
                         assigned_to    VARCHAR,
                         estimated_time DOUBLE  NOT NULL,
                         resting_time   DOUBLE  NOT NULL,
                         done_time      DOUBLE  NOT NULL    DEFAULT 0,
                         FOREIGN KEY (sprint_id) REFERENCES Sprints (id),
                         FOREIGN KEY (activity_id) REFERENCES Activities (id),
                         FOREIGN KEY (project_id) REFERENCES Projects (id),
                         UNIQUE (tfs_number, sprint_id)
                     )
                     """)

        # Log table
        conn.execute("""
                     CREATE TABLE Logs
                     (
                         id          INTEGER PRIMARY KEY DEFAULT nextval('seq_log_id'),
                         task_id     INTEGER NOT NULL,
                         week_number INTEGER NOT NULL,
                         log_date    DATE    NOT NULL,
                         logged_time DOUBLE  NOT NULL,
                         notes       VARCHAR,
                         FOREIGN KEY (task_id) REFERENCES Tasks (id)
                     )
                     """)
        conn.commit()
        print("✓ Database created successfully")
    else:
        print(f"Using existing DB at {DB_PATH}")
    conn.close()


def get_connection():
    """Get a connection to the database. Initializes it if needed."""
    try:
        duckdb.connect(str(DB_PATH)).close()
    except duckdb.DatabaseError:
        print("Database not found, initializing new database")
        init_db()
    return duckdb.connect(str(DB_PATH))


def delete_database():
    """Delete database if needed."""
    try:
        os.remove(str(DB_PATH))
        print("Database deleted successfully.")
    except FileNotFoundError:
        raise IOError(f"Database file not found")
    except PermissionError:
        raise PermissionError("Database still in use. Please, close connection and retry.")

if __name__ == "__main__":
    init_db()
    conn = get_connection()
    conn.close()
    delete_database()