from src.backend.database.db import *
from src.backend.repositories.task_repository import *
from src.backend.repositories.sprint_repository import *

if __name__ == "__main__":
    try:
        delete_database()
    except Exception as e:
        print(f"Exception: {e}")
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
    repo.create_task("0002",
                     "test_2",
                     2,
                     1,
                     2,
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
        repo.find_by_id(1),15
    )