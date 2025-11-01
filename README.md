# tYme-logger

Application to help to log time in my daily job.

I need to be able to import extracts from TFS and to log some time for each week on it.

For the db, I will use a duckdb file in my `~/.local/tyme-logger/` folder.

## Entities

### Task
- **Id**
- **TfsNumber** (TFS identifier for import matching)
- **SprintId** (FK to Sprint)
- **Project**
- **Activity**
- **Status**
- **AssignedTo**
- **EstimatedTime** (initial estimation)
- **RestingTime** (time remaining to do)
- **DoneTime** (time consumed/realized)

*Note: If a task spans multiple sprints (overflow), it's duplicated with different SprintId*

### Sprint
- **Id**
- **TfsNumber** (TFS identifier for import matching)
- **Code**
- **StartingDate**
- **EndingDate**

### Log
- **Id**
- **TaskId** (FK to Task)
- **WeekNumber** (ISO week number, deduced from LogDate)
- **LogDate** (any day within the week, date picker selects the week)
- **LoggedTime** (amount of time logged)
- **Notes** (optional, why this time was logged)
- **Source** (imported / manual)

## Two-level Reading

### 1. By Week (Project + Activity)
*"I logged 2h today on this task → cumulative Xh on <project> - <activity> this week"*

```sql
SELECT Project, Activity, SUM(LoggedTime) as weekly_time
FROM Log 
JOIN Task ON Log.TaskId = Task.Id
WHERE LogDate BETWEEN :week_start AND :week_end
GROUP BY Project, Activity
ORDER BY Project, Activity
```

### 2. By Sprint (Task level)
*"I logged 2h today on this task → cumulative Xh on this task for the entire sprint"*

```sql
SELECT Task.Id, Task.Activity, SUM(LoggedTime) as sprint_time
FROM Log
JOIN Task ON Log.TaskId = Task.Id
WHERE Task.SprintId = :sprint_id
GROUP BY Task.Id, Task.Activity
ORDER BY Task.Id
```

## Features

- [x] Init database
- [ ] Import extracts from TFS
- [ ] Manual time logging
- [ ] Weekly aggregation by (Project, Activity)
- [ ] Sprint aggregation by Task
- [ ] Handle task overflow across sprints