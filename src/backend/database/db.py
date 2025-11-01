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
        conn.execute("CREATE SEQUENCE seq_sprint_id START 1")
        conn.execute("CREATE SEQUENCE seq_task_id START 1")
        conn.execute("CREATE SEQUENCE seq_log_id START 1")

        # Sprint table
        conn.execute("""
                     CREATE TABLE Sprint
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
                     CREATE TABLE Task
                     (
                         id             INTEGER PRIMARY KEY DEFAULT nextval('seq_task_id'),
                         tfs_number     VARCHAR NOT NULL,
                         sprint_id      INTEGER NOT NULL,
                         project        VARCHAR NOT NULL,
                         activity       VARCHAR NOT NULL,
                         status         VARCHAR NOT NULL,
                         assigned_to    VARCHAR,
                         estimated_time DOUBLE  NOT NULL,
                         resting_time   DOUBLE  NOT NULL,
                         done_time      DOUBLE  NOT NULL    DEFAULT 0,
                         FOREIGN KEY (sprint_id) REFERENCES Sprint (id),
                         UNIQUE (tfs_number, sprint_id)
                     )
                     """)

        # Log table
        conn.execute("""
                     CREATE TABLE Log
                     (
                         id          INTEGER PRIMARY KEY DEFAULT nextval('seq_log_id'),
                         task_id     INTEGER NOT NULL,
                         week_number INTEGER NOT NULL,
                         log_date    DATE    NOT NULL,
                         logged_time DOUBLE  NOT NULL,
                         notes       VARCHAR,
                         source      VARCHAR NOT NULL CHECK (source IN ('imported', 'manual')),
                         FOREIGN KEY (task_id) REFERENCES Task (id)
                     )
                     """)

        conn.commit()
        print("✓ Schema created successfully")
    else:
        print(f"Database already exists at {DB_PATH}")

    conn.close()


if __name__ == "__main__":
    init_db()