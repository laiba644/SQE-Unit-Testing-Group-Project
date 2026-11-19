"""Strict SQE per-function test suite: 5 distinct inputs per function for this allocation.

OWNER PLACEHOLDER: Students must review/extend their own allocated cases and commit
from their own Git accounts. This generated allocation is not contribution evidence.
"""
import sqlite3
import pytest
import db
import task_service as svc
import task_validation as val

@pytest.fixture
def isolated_db(tmp_path, monkeypatch):
    monkeypatch.chdir(__import__('pathlib').Path(__file__).resolve().parents[1])
    path = str(tmp_path / 'strict.db')
    db.init_db(path)
    return path

def seed(path, title='Seed', description='Desc', due_date='2026-10-20', status='pending'):
    db.create_task(title, description, due_date, status, path)
    return db.get_all_tasks(path)[-1]['id']


@pytest.mark.parametrize("case", [
    ('   ',None,ValueError),
    ('  Work  ','Work',None),
    ('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX','XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',None),
    (55,None,TypeError),
    ('  Z  ','Z',None),
], ids=['B-validate_title-01', 'B-validate_title-02', 'B-validate_title-03', 'B-validate_title-04', 'B-validate_title-05'])
def test_validate_title_b(case):
    value, expected, error = case
    if error:
        with pytest.raises(error): val.validate_title(value)
    else: assert val.validate_title(value) == expected

@pytest.mark.parametrize("case", [
    ('2000-02-29','2000-02-29',None),
    ('1900-02-29',None,ValueError),
    ('2026-13-01',None,ValueError),
    ('2026-10-1',None,ValueError),
    (123,None,TypeError),
], ids=['B-validate_due_date-01', 'B-validate_due_date-02', 'B-validate_due_date-03', 'B-validate_due_date-04', 'B-validate_due_date-05'])
def test_validate_due_date_b(case):
    value, expected, error = case
    if error:
        with pytest.raises(error): val.validate_due_date(value)
    else: assert val.validate_due_date(value) == expected

@pytest.mark.parametrize("case", [
    ('PENDING',None,ValueError),
    (' completed ',None,ValueError),
    (1,None,ValueError),
    (True,None,ValueError),
    ('pending','pending',None),
], ids=['B-validate_status-01', 'B-validate_status-02', 'B-validate_status-03', 'B-validate_status-04', 'B-validate_status-05'])
def test_validate_status_b(case):
    value, expected, error = case
    if error:
        with pytest.raises(error): val.validate_status(value)
    else: assert val.validate_status(value) == expected

@pytest.mark.parametrize("case", [
    ('  Work  ','trim','2026-10-20','pending','Work',None),
    ('Valid','','2026-10-20','bad',None,ValueError),
    ('YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY','','2026-10-20','pending',None,ValueError),
    ('Title','','2028-02-29','pending','Title',None),
    (None,'','2026-10-20','pending',None,TypeError),
], ids=['B-add_task-01', 'B-add_task-02', 'B-add_task-03', 'B-add_task-04', 'B-add_task-05'])
def test_add_task_b(case, isolated_db):
    title, description, date, status, expected, error = case
    if error:
        with pytest.raises(error): svc.add_task(title, description, date, status, isolated_db)
        assert svc.list_tasks(isolated_db) == []
    else:
        record=svc.add_task(title, description, date, status, isolated_db)
        assert record['title'] == expected and record['description'] == description
        assert len(svc.list_tasks(isolated_db)) == 1

@pytest.mark.parametrize("case", [
    ['Solo'],
    ['T1','T2','T3','T4'],
    ['same','same','same'],
    [' Z '],
    ['0','1','2','3','4'],
], ids=['B-list_tasks-01', 'B-list_tasks-02', 'B-list_tasks-03', 'B-list_tasks-04', 'B-list_tasks-05'])
def test_list_tasks_b(case, isolated_db):
    titles=case
    for title in titles: seed(isolated_db,title)
    assert [x['title'] for x in svc.list_tasks(isolated_db)] == titles

@pytest.mark.parametrize("case", [
    (1,True,'error'),
    (1,'1','error'),
    (1,None,'error'),
    (1,999,'none'),
    (3,3,'found'),
], ids=['B-find_task-01', 'B-find_task-02', 'B-find_task-03', 'B-find_task-04', 'B-find_task-05'])
def test_find_task_b(case, isolated_db):
    count, requested, expected = case
    ids=[seed(isolated_db, 'Item'+str(i)) for i in range(count)]
    if expected == 'error':
        with pytest.raises(ValueError): svc.find_task(requested, isolated_db)
    elif expected == 'none': assert svc.find_task(requested, isolated_db) is None
    else:
        task=svc.find_task(ids[requested-1], isolated_db)
        assert task['title'] == 'Item'+str(requested-1)

@pytest.mark.parametrize("case", [
    ('completed','completed',False,'completed',None),
    ('pending','PENDING',False,None,ValueError),
    ('pending',None,False,None,ValueError),
    ('completed','pending',True,None,None),
    ('completed','completed',True,None,None),
], ids=['B-change_status-01', 'B-change_status-02', 'B-change_status-03', 'B-change_status-04', 'B-change_status-05'])
def test_change_status_b(case, isolated_db):
    initial, target, missing, expected, error=case
    task_id = seed(isolated_db, status=initial)
    if error:
        with pytest.raises(error): svc.change_status(task_id, target, isolated_db)
        assert db.get_task_by_id(task_id, isolated_db)['status'] == initial
    elif missing: assert svc.change_status(task_id+999, target, isolated_db) is None
    else:
        assert svc.change_status(task_id,target,isolated_db)['status']==expected
        assert db.get_task_by_id(task_id,isolated_db)['status']==expected

@pytest.mark.parametrize("case", [
    (2,1,True),
    (3,2,True),
    (1,500,False),
    (0,500,False),
    (3,0,True),
], ids=['B-remove_task-01', 'B-remove_task-02', 'B-remove_task-03', 'B-remove_task-04', 'B-remove_task-05'])
def test_remove_task_b(case, isolated_db):
    count, select, expected=case
    ids=[seed(isolated_db,'Entry'+str(i)) for i in range(count)]
    if select == 'invalid':
        with pytest.raises(ValueError): svc.remove_task(0,isolated_db)
    else:
        task_id=ids[select] if isinstance(select,int) and select < len(ids) else 99999
        assert svc.remove_task(task_id,isolated_db) is expected
        assert len(db.get_all_tasks(isolated_db)) == count-int(expected)

@pytest.mark.parametrize("case", [
    'columns',
    'table',
    'fresh',
    'retain',
    'repeated',
], ids=['B-init_db-01', 'B-init_db-02', 'B-init_db-03', 'B-init_db-04', 'B-init_db-05'])
def test_init_db_b(case, isolated_db):
    mode=case
    if mode=='fresh': assert db.get_all_tasks(isolated_db)==[]
    elif mode=='repeated': db.init_db(isolated_db); assert db.get_all_tasks(isolated_db)==[]
    elif mode=='retain': seed(isolated_db); db.init_db(isolated_db); assert len(db.get_all_tasks(isolated_db))==1
    elif mode=='columns':
        with sqlite3.connect(isolated_db) as c: assert {'id','title','status'}.issubset({x[1] for x in c.execute('PRAGMA table_info(tasks)')})
    else:
        with sqlite3.connect(isolated_db) as c: assert c.execute('SELECT count(*) FROM sqlite_master WHERE type="table" AND name="tasks"').fetchone()[0]==1

@pytest.mark.parametrize("case", [
    ('Task',None,'2026-10-21','pending',None),
    ('Task','',None,'pending',None),
    ('Task','','2026-10-21','completed',None),
    ('Task','','2026-10-21',None,sqlite3.IntegrityError),
    ('ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ','long','2026-10-21','pending',None),
], ids=['B-create_task-01', 'B-create_task-02', 'B-create_task-03', 'B-create_task-04', 'B-create_task-05'])
def test_create_task_b(case, isolated_db):
    title, desc, date, status, error=case
    if error:
        with pytest.raises(error): db.create_task(title,desc,date,status,isolated_db)
        assert db.get_all_tasks(isolated_db)==[]
    else:
        db.create_task(title,desc,date,status,isolated_db)
        row=db.get_all_tasks(isolated_db)[0]
        assert (row['title'],row['description'],row['due_date'],row['status'])==(title,desc,date,status)

@pytest.mark.parametrize("case", [
    ['Z'],
    ['Z','Y'],
    ['1','2','3','4'],
    ['X','X','X','X','X','X'],
    [],
], ids=['B-get_all_tasks-01', 'B-get_all_tasks-02', 'B-get_all_tasks-03', 'B-get_all_tasks-04', 'B-get_all_tasks-05'])
def test_get_all_tasks_b(case, isolated_db):
    titles=case
    for title in titles: seed(isolated_db,title)
    rows=db.get_all_tasks(isolated_db)
    assert len(rows)==len(titles) and [x['title'] for x in rows]==titles

@pytest.mark.parametrize("case", [
    (2,0,'found'),
    (3,2,'found'),
    (2,5000,'none'),
    (1,-1,'none'),
    (0,0,'none'),
], ids=['B-get_task_by_id-01', 'B-get_task_by_id-02', 'B-get_task_by_id-03', 'B-get_task_by_id-04', 'B-get_task_by_id-05'])
def test_get_task_by_id_b(case, isolated_db):
    count, offset, expected=case
    ids=[seed(isolated_db, 'Item'+str(i)) for i in range(count)]
    task_id=ids[offset] if isinstance(offset,int) and 0 <= offset < count else offset
    record=db.get_task_by_id(task_id,isolated_db)
    assert (record is None) == (expected=='none')
    if record is not None: assert record['id']==task_id

@pytest.mark.parametrize("case", [
    ('Name','New name','existing','New name'),
    ('A','XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX','existing','XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'),
    ('Alpha','Beta','missing','Alpha'),
    ('First','Second','existing','Second'),
    ('Y','Y','missing','Y'),
], ids=['B-update_task-01', 'B-update_task-02', 'B-update_task-03', 'B-update_task-04', 'B-update_task-05'])
def test_update_task_b(case, isolated_db):
    initial, change, selector, expected=case
    task_id=seed(isolated_db,title=initial)
    target=task_id if selector=='existing' else task_id+1000
    db.update_task(target,change,'Edited','2027-01-02','completed',isolated_db)
    record=db.get_task_by_id(task_id,isolated_db)
    assert record['title']==expected
    assert record['status']==('completed' if selector=='existing' else 'pending')

@pytest.mark.parametrize("case", [
    (2,1,1),
    (3,0,2),
    (3,10,3),
    (1,1,1),
    (4,3,3),
], ids=['B-delete_task-01', 'B-delete_task-02', 'B-delete_task-03', 'B-delete_task-04', 'B-delete_task-05'])
def test_delete_task_b(case, isolated_db):
    count, selected, remaining=case
    ids=[seed(isolated_db,'D'+str(i)) for i in range(count)]
    target=ids[selected] if selected < count else 99999
    db.delete_task(target, isolated_db)
    assert len(db.get_all_tasks(isolated_db))==remaining
    if selected < count: assert db.get_task_by_id(target,isolated_db) is None

@pytest.mark.parametrize("mode", ['named_row', 'commit', 'readback', 'wal', 'table'], ids=['B-get_connection-01', 'B-get_connection-02', 'B-get_connection-03', 'B-get_connection-04', 'B-get_connection-05'])
def test_get_connection_b(mode, isolated_db):
    conn=db.get_connection(isolated_db)
    try:
        if mode in ('row_factory','named_row'):
            assert conn.row_factory is sqlite3.Row
        elif mode in ('journal','wal'):
            assert conn.execute('PRAGMA journal_mode').fetchone()[0].lower() == 'wal'
        elif mode in ('writable','commit'):
            conn.execute("INSERT INTO tasks (title,description,due_date,status) VALUES ('W','', '2026-01-01','pending')")
            conn.commit()
            assert db.get_all_tasks(isolated_db)[0]['title']=='W'
        elif mode in ('separate','readback'):
            other=db.get_connection(isolated_db)
            try: assert other is not conn and other.execute('SELECT count(*) FROM tasks').fetchone()[0]==0
            finally: other.close()
        elif mode in ('schema','table'):
            assert conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tasks'").fetchone()[0]=='tasks'
    finally:
        conn.close()
