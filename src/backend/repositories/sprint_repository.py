from src.backend.database.db import get_connection
from src.backend.models.sprint import Sprint
from datetime import date

class SprintRepository:
    """How to deal with Sprint table"""

    def find_by_id(self, sprint_id: int) -> Sprint | None:
        conn = get_connection()
        result = conn.execute("""
        SELECT id, tfs_number, code, starting_date, ending_date FROM Sprints WHERE Id = ?
        """, (sprint_id,)).fetchone()
        conn.close()
        if not result:
            return None
        _id, _tfs_number, _code, _starting_date, _ending_date = result
        return Sprint(
            id=_id,
            tfs_number=_tfs_number,
            code=_code,
            starting_date=_starting_date,
            ending_date=_ending_date
        )

    def find_by_tfs(self, tfs_number: int) -> Sprint | None:
        conn = get_connection()
        result = conn.execute("""
        SELECT id, tfs_number, code, starting_date, ending_date FROM Sprints WHERE tfs_number = ?
        """, (tfs_number,)).fetchone()
        conn.close()
        if not result:
            return None
        _id, _tfs_number, _code, _starting_date, _ending_date = result
        return Sprint(
            id=_id,
            tfs_number=_tfs_number,
            code=_code,
            starting_date=_starting_date,
            ending_date=_ending_date
        )

    def find_all(self) -> list[Sprint] | None:
        conn = get_connection()
        results = conn.execute("""
        SELECT id, tfs_number, code, starting_date, ending_date FROM Sprints
        """).fetchall()
        conn.close()
        if not results:
            return None
        return [
            Sprint(
                id=r[0],
                tfs_number=r[1],
                code=r[2],
                starting_date=r[3],
                ending_date=r[4]
            )
            for r in results
        ]

    def find_active(self, today: date = None) -> Sprint | list[Sprint] | None:
        """Récupère les sprints actifs (aujourd'hui entre starting_date et ending_date)"""
        if today is None:
            today = date.today()

        conn = get_connection()
        results = conn.execute(
            "SELECT id, tfs_number, code, starting_date, ending_date FROM Sprints WHERE starting_date <= ? AND ending_date >= ?",
            (today, today)
        ).fetchall()
        conn.close()
        if not results:
            return None
        if len(results) == 1:
            _id, _tfs_number, _code, _starting_date, _ending_date = results[0]
            return Sprint(
                id=_id,
                tfs_number=_tfs_number,
                code=_code,
                starting_date=_starting_date,
                ending_date=_ending_date
            )
        return [
            Sprint(
                id=r[0],
                tfs_number=r[1],
                code=r[2],
                starting_date=r[3],
                ending_date=r[4]
            ) for r in results
        ]

    def create_sprint(self, tfs_number: str, code: str, starting_date: date, ending_date: date) -> Sprint:
        conn = get_connection()
        try:
            conn.execute("""
            INSERT INTO Sprints (tfs_number, code, starting_date, ending_date)
                VALUES (?, ?, ?, ?)
            """, (tfs_number, code, starting_date, ending_date))
        except Exception as e:
            print(e)
            return None

        _id = conn.execute("SELECT id FROM sprints where tfs_number = ?", (tfs_number,)).fetchone()[0]
        conn.close()

        return Sprint(
            id=_id,
            tfs_number=tfs_number,
            code=code,
            starting_date=starting_date,
            ending_date=ending_date
        )

if __name__ == "__main__":
    repo = SprintRepository()
    repo.create_sprint("0001",
                       "test",
                       date(2023, 1, 1),
                       date(2023, 1, 10)
                       )
    repo.create_sprint("0002",
                       "test_2",
                       date(2023, 1, 11),
                       date(2023, 1, 20)
                       )
    repo.create_sprint("0003",
                       "test_3",
                       date(2023, 1, 21),
                       date(2023, 1, 30)
                       )