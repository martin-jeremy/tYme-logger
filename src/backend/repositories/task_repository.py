from src.backend.database.db import get_connection
from src.backend.models.task import Task


class TaskRepository:
    """How to deal with Task table"""

    def find_by_id(self, task_id: int) -> Task | None:
        conn = get_connection()
        result = conn.execute("""
                              SELECT id
                                   , tfs_number
                                   , description
                                   , sprint_id
                                   , project_id
                                   , activity_id
                                   , status
                                   , assigned_to
                                   , estimated_time
                                   , resting_time
                                   , done_time
                              FROM Tasks WHERE Id = ?
                              """, (task_id,)).fetchone()
        conn.close()
        if not result:
            return None
        _id, _tfs_number, _desc, _sprint_id, _project_id, _activity_id, _status, _assigned_to, _estimated_time, _resting_time, _done_time = result
        return Task(
            id=_id,
            tfs_number=_tfs_number,
            description=_desc,
            sprint_id=_sprint_id,
            project_id=_project_id,
            activity_id=_activity_id,
            status=_status,
            assigned_to=_assigned_to,
            estimated_time=_estimated_time,
            resting_time=_resting_time,
            done_time=_done_time
        )


    def find_by_tfs(self, tfs_number: int) -> Task | None:
        conn = get_connection()
        result = conn.execute("""
                              SELECT id
                                   , tfs_number
                                   , description
                                   , sprint_id
                                   , project_id
                                   , activity_id
                                   , status
                                   , assigned_to
                                   , estimated_time
                                   , resting_time
                                   , done_time
                              FROM Tasks WHERE tfs_number = ?
                              """, (tfs_number,)).fetchone()
        conn.close()

        if not result:
            return None

        _id, _tfs_number, _desc, _sprint_id, _project_id, _activity_id, _status, _assigned_to, _estimated_time, _resting_time, _done_time = result
        return Task(
            id=_id,
            tfs_number=_tfs_number,
            description=_desc,
            sprint_id=_sprint_id,
            project_id=_project_id,
            activity_id=_activity_id,
            status=_status,
            assigned_to=_assigned_to,
            estimated_time=_estimated_time,
            resting_time=_resting_time,
            done_time=_done_time
        )


    def find_by_sprint_id(self, sprint_id: int) -> list[Task] | None:
        conn = get_connection()
        results = conn.execute("""
                               SELECT id
                                    , tfs_number
                                    , description
                                    , sprint_id
                                    , project_id
                                    , activity_id
                                    , status
                                    , assigned_to
                                    , estimated_time
                                    , resting_time
                                    , done_time
                               FROM Tasks WHERE sprint_id = ?
                               """, (sprint_id,)).fetchall()
        conn.close()

        if not results:
            return None

        return [
            Task(
                id=r[0],
                tfs_number=r[1],
                description=r[2],
                sprint_id=r[3],
                project_id=r[4],
                activity_id=r[5],
                status=r[6],
                assigned_to=r[7],
                estimated_time=r[8],
                resting_time=r[9],
                done_time=r[10]
            )
            for r in results
        ]


    def find_by_tfs_sprint(self, sprint_tfs_number: str) -> list[Task] | None:
        conn = get_connection()
        sprint_id = conn.execute("""
                                 SELECT id FROM Sprints WHERE tfs_number = ?
                                 """, (sprint_tfs_number,)).fetchone()[0]
        results = conn.execute("""
                               SELECT id
                                    , tfs_number
                                    , description
                                    , sprint_id
                                    , project_id
                                    , activity_id
                                    , status
                                    , assigned_to
                                    , estimated_time
                                    , resting_time
                                    , done_time
                               FROM Tasks
                               WHERE sprint_id = ?
                               """, (sprint_id,)).fetchall()
        if not results:
            return None

        return [
            Task(
                id=r[0],
                tfs_number=r[1],
                description=r[2],
                sprint_id=r[3],
                project_id=r[4],
                activity_id=r[5],
                status=r[6],
                assigned_to=r[7],
                estimated_time=r[8],
                resting_time=r[9],
                done_time=r[10]
            )
            for r in results
        ]


    def create_task(self, tfs_number: str, description: str, sprint_id: int, project_id: int, activity_id: int, status: str, assigned_to: str, estimated_time: int, resting_time: int, done_time: int) -> Task:
        conn = get_connection()
        conn.execute("""
                      INSERT INTO Tasks (tfs_number, description, sprint_id, project_id, activity_id, status, assigned_to, estimated_time, resting_time, done_time)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                      """, (tfs_number, description, sprint_id, project_id, activity_id, status, assigned_to, estimated_time, resting_time, done_time))
        _id = conn.execute("SELECT id FROM tasks where tfs_number = ?", (tfs_number,)).fetchone()[0]
        conn.close()
        return Task(
            id=_id,
            tfs_number=tfs_number,
            description=description,
            sprint_id=sprint_id,
            project_id=project_id,
            activity_id=activity_id,
            status=status,
            assigned_to=assigned_to,
            estimated_time=estimated_time,
            resting_time=resting_time,
            done_time=done_time
        )


    def add_time(self, task: Task, to_add: float) -> Task:
        new_done = task.done_time + to_add
        new_resting = max(task.resting_time - to_add, 0)
        conn = get_connection()
        conn.execute("""
                      UPDATE Tasks
                      SET done_time = ?,
                          resting_time = ?
                      WHERE id = ?
        """, (new_done, new_resting, task.id))
        conn.close()
        return Task(
            id=task.id,
            tfs_number=task.tfs_number,
            description=task.description,
            sprint_id=task.sprint_id,
            project_id=task.project_id,
            activity_id=task.activity_id,
            status=task.status,
            assigned_to=task.assigned_to,
            estimated_time=task.estimated_time,
            resting_time=new_resting,
            done_time=new_done
        )


    def remove_time(self, task: Task, to_remove: float) -> Task:
        new_done = task.done_time - to_remove
        new_resting = max(task.resting_time + to_remove, 0, task.estimated_time - task.resting_time + to_remove)
        conn = get_connection()
        conn.execute("""
                      UPDATE Tasks
                      SET done_time = ?,
                          resting_time = ?
                      WHERE id = ?
        """, (new_done, new_resting, task.id))
        conn.close()
        return Task(
            id=task.id,
            tfs_number=task.tfs_number,
            description=task.description,
            sprint_id=task.sprint_id,
            project_id=task.project_id,
            activity_id=task.activity_id,
            status=task.status,
            assigned_to=task.assigned_to,
            estimated_time=task.estimated_time,
            resting_time=new_resting,
            done_time=new_done
        )


if __name__ == "__main__":
    repo = TaskRepository()
    repo.create_task("0001",
                      "test",
                      1,
                      1,
                      1,
                      "En cours",
                      "Jeremy",
                      10,
                      10,
                     0
    )
    repo.find_by_id(1)
    repo.find_by_tfs("0001")
    repo.find_by_sprint_id(1)
    repo.find_by_tfs_sprint("0001")
    repo.add_time(
        repo.find_by_id(1),2
    )