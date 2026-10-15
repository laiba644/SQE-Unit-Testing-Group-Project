"""Framework-independent task operations built on the original db.py."""
import db
from task_validation import validate_title, validate_due_date, validate_status


def add_task(title, description, due_date, status='pending', db_name='tasks.db'):
    title = validate_title(title)
    due_date = validate_due_date(due_date)
    status = validate_status(status)
    if not isinstance(description, str):
        raise TypeError('description must be a string')
    db.create_task(title, description, due_date, status, db_name)
    return db.get_all_tasks(db_name)[-1]


def list_tasks(db_name='tasks.db'):
    return db.get_all_tasks(db_name)


def find_task(task_id, db_name='tasks.db'):
    if not isinstance(task_id, int) or isinstance(task_id, bool) or task_id <= 0:
        raise ValueError('task_id must be a positive integer')
    return db.get_task_by_id(task_id, db_name)


def change_status(task_id, status, db_name='tasks.db'):
    status = validate_status(status)
    task = find_task(task_id, db_name)
    if task is None:
        return None
    db.update_task(task_id, task['title'], task['description'], task['due_date'], status, db_name)
    return db.get_task_by_id(task_id, db_name)


def remove_task(task_id, db_name='tasks.db'):
    task = find_task(task_id, db_name)
    if task is None:
        return False
    db.delete_task(task_id, db_name)
    return True
