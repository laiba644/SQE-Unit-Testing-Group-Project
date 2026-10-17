
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
    ('','',ValueError),
    ('A','A',None),
    ('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX','XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',None),
    ('YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY',None,ValueError),
    (None,None,TypeError),
], ids=['A-validate_title-01', 'A-validate_title-02', 'A-validate_title-03', 'A-validate_title-04', 'A-validate_title-05'])
def test_validate_title_a(case):
    value, expected, error = case
    if error:
        with pytest.raises(error): val.validate_title(value)
    else: assert val.validate_title(value) == expected

@pytest.mark.parametrize("case", [
    ('2028-02-29','2028-02-29',None),
    ('2027-02-29',None,ValueError),
    ('2026-01-01','2026-01-01',None),
    ('',None,ValueError),
    (None,None,TypeError),
], ids=['A-validate_due_date-01', 'A-validate_due_date-02', 'A-validate_due_date-03', 'A-validate_due_date-04', 'A-validate_due_date-05'])
def test_validate_due_date_a(case):
    value, expected, error = case
    if error:
        with pytest.raises(error): val.validate_due_date(value)
    else: assert val.validate_due_date(value) == expected

@pytest.mark.parametrize("case", [
    ('pending','pending',None),
    ('completed','completed',None),
    ('unknown',None,ValueError),
    ('',None,ValueError),
    (None,None,ValueError),
], ids=['A-validate_status-01', 'A-validate_status-02', 'A-validate_status-03', 'A-validate_status-04', 'A-validate_status-05'])
def test_validate_status_a(case):
    value, expected, error = case
    if error:
        with pytest.raises(error): val.validate_status(value)
    else: assert val.validate_status(value) == expected

@pytest.mark.parametrize("case", [
    ('A','','2026-10-20','pending','A',None),
    ('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX','long','2026-10-20','completed','XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',None),
    ('','','2026-10-20','pending',None,ValueError),
    ('OK','desc','2026-02-30','pending',None,ValueError),
    ('Fine',7,'2026-10-20','pending',None,TypeError),
], ids=['A-add_task-01', 'A-add_task-02', 'A-add_task-03', 'A-add_task-04', 'A-add_task-05'])
def test_add_task_a(case, isolated_db):
    title, description, date, status, expected, error = case
    if error:
        with pytest.raises(error): svc.add_task(title, description, date, status, isolated_db)
        assert svc.list_tasks(isolated_db) == []
    else:
        record=svc.add_task(title, description, date, status, isolated_db)
        assert record['title'] == expected and record['description'] == description
        assert len(svc.list_tasks(isolated_db)) == 1

@pytest.mark.parametrize("case", [
    [],
    ['One'],
    ['A','B'],
    ['A','B','C'],
    ['Repeated','Repeated'],
], ids=['A-list_tasks-01', 'A-list_tasks-02', 'A-list_tasks-03', 'A-list_tasks-04', 'A-list_tasks-05'])
def test_list_tasks_a(case, isolated_db):
    titles=case
    for title in titles: seed(isolated_db,title)
    assert [x['title'] for x in svc.list_tasks(isolated_db)] == titles

@pytest.mark.parametrize("case", [
    (0,1,'none'),
    (1,1,'found'),
    (2,2,'found'),
    (1,0,'error'),
    (1,-1,'error'),
], ids=['A-find_task-01', 'A-find_task-02', 'A-find_task-03', 'A-find_task-04', 'A-find_task-05'])
def test_find_task_a(case, isolated_db):
    count, requested, expected = case
    ids=[seed(isolated_db, 'Item'+str(i)) for i in range(count)]
    if expected == 'error':
        with pytest.raises(ValueError): svc.find_task(requested, isolated_db)
    elif expected == 'none': assert svc.find_task(requested, isolated_db) is None
    else:
        task=svc.find_task(ids[requested-1], isolated_db)
        assert task['title'] == 'Item'+str(requested-1)

@pytest.mark.parametrize("case", [
    ('pending','completed',False,'completed',None),
    ('completed','pending',False,'pending',None),
    ('pending','completed',True,None,None),
    ('pending','unknown',False,None,ValueError),
    ('pending','pending',False,'pending',None),
], ids=['A-change_status-01', 'A-change_status-02', 'A-change_status-03', 'A-change_status-04', 'A-change_status-05'])
def test_change_status_a(case, isolated_db):
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
    (1,0,True),
    (1,999,False),
    (2,0,True),
    (0,999,False),
    (1,'invalid',False),
], ids=['A-remove_task-01', 'A-remove_task-02', 'A-remove_task-03', 'A-remove_task-04', 'A-remove_task-05'])
def test_remove_task_a(case, isolated_db):
    count, select, expected=case
    ids=[seed(isolated_db,'Entry'+str(i)) for i in range(count)]
    if select == 'invalid':
        with pytest.raises(ValueError): svc.remove_task(0,isolated_db)
    else:
        task_id=ids[select] if isinstance(select,int) and select < len(ids) else 99999
        assert svc.remove_task(task_id,isolated_db) is expected
        assert len(db.get_all_tasks(isolated_db)) == count-int(expected)

@pytest.mark.parametrize("case", [
    'fresh',
    'repeated',
    'retain',
    'columns',
    'table',
], ids=['A-init_db-01', 'A-init_db-02', 'A-init_db-03', 'A-init_db-04', 'A-init_db-05'])
def test_init_db_a(case, isolated_db):
    mode=case
    if mode=='fresh': assert db.get_all_tasks(isolated_db)==[]
    elif mode=='repeated': db.init_db(isolated_db); assert db.get_all_tasks(isolated_db)==[]
    elif mode=='retain': seed(isolated_db); db.init_db(isolated_db); assert len(db.get_all_tasks(isolated_db))==1
    elif mode=='columns':
        with sqlite3.connect(isolated_db) as c: assert {'id','title','status'}.issubset({x[1] for x in c.execute('PRAGMA table_info(tasks)')})
    else:
        with sqlite3.connect(isolated_db) as c: assert c.execute('SELECT count(*) FROM sqlite_master WHERE type="table" AND name="tasks"').fetchone()[0]==1

@pytest.mark.parametrize("case", [
    ('A','','2026-10-21','pending',None),
    ('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX','d','2026-10-21','completed',None),
    (None,'d','2026-10-21','pending',sqlite3.IntegrityError),
    ('C','','2026-10-21','bad',sqlite3.IntegrityError),
    ('','empty','2026-10-21','pending',None),
], ids=['A-create_task-01', 'A-create_task-02', 'A-create_task-03', 'A-create_task-04', 'A-create_task-05'])
def test_create_task_a(case, isolated_db):
    title, desc, date, status, error=case
    if error:
        with pytest.raises(error): db.create_task(title,desc,date,status,isolated_db)
        assert db.get_all_tasks(isolated_db)==[]
    else:
        db.create_task(title,desc,date,status,isolated_db)
        row=db.get_all_tasks(isolated_db)[0]
        assert (row['title'],row['description'],row['due_date'],row['status'])==(title,desc,date,status)

@pytest.mark.parametrize("case", [
    [],
    ['One'],
    ['One','Two'],
    ['A','B','C'],
    ['Same','Same'],
], ids=['A-get_all_tasks-01', 'A-get_all_tasks-02', 'A-get_all_tasks-03', 'A-get_all_tasks-04', 'A-get_all_tasks-05'])
def test_get_all_tasks_a(case, isolated_db):
    titles=case
    for title in titles: seed(isolated_db,title)
    rows=db.get_all_tasks(isolated_db)
    assert len(rows)==len(titles) and [x['title'] for x in rows]==titles

@pytest.mark.parametrize("case", [
    (0,999,'none'),
    (1,0,'found'),
    (2,1,'found'),
    (1,999,'none'),
    (3,2,'found'),
], ids=['A-get_task_by_id-01', 'A-get_task_by_id-02', 'A-get_task_by_id-03', 'A-get_task_by_id-04', 'A-get_task_by_id-05'])
def test_get_task_by_id_a(case, isolated_db):
    count, offset, expected=case
    ids=[seed(isolated_db, 'Item'+str(i)) for i in range(count)]
    task_id=ids[offset] if isinstance(offset,int) and 0 <= offset < count else offset
    record=db.get_task_by_id(task_id,isolated_db)
    assert (record is None) == (expected=='none')
    if record is not None: assert record['id']==task_id

@pytest.mark.parametrize("case", [
    ('Start','Edited','existing','Edited'),
    ('Start','','existing',''),
    ('Start','New','missing','Start'),
    ('One','One','existing','One'),
    ('A','XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX','existing','XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'),
], ids=['A-update_task-01', 'A-update_task-02', 'A-update_task-03', 'A-update_task-04', 'A-update_task-05'])
def test_update_task_a(case, isolated_db):
    initial, change, selector, expected=case
    task_id=seed(isolated_db,title=initial)
    target=task_id if selector=='existing' else task_id+1000
    db.update_task(target,change,'Edited','2027-01-02','completed',isolated_db)
    record=db.get_task_by_id(task_id,isolated_db)
    assert record['title']==expected
    assert record['status']==('completed' if selector=='existing' else 'pending')

@pytest.mark.parametrize("case", [
    (0,0,0),
    (1,0,0),
    (1,10,1),
    (2,0,1),
    (3,2,2),
], ids=['A-delete_task-01', 'A-delete_task-02', 'A-delete_task-03', 'A-delete_task-04', 'A-delete_task-05'])
def test_delete_task_a(case, isolated_db):
    count, selected, remaining=case
    ids=[seed(isolated_db,'D'+str(i)) for i in range(count)]
    target=ids[selected] if selected < count else 99999
    db.delete_task(target, isolated_db)
    assert len(db.get_all_tasks(isolated_db))==remaining
    if selected < count: assert db.get_task_by_id(target,isolated_db) is None

@pytest.mark.parametrize("mode", ['row_factory', 'writable', 'journal', 'separate', 'schema'], ids=['A-get_connection-01', 'A-get_connection-02', 'A-get_connection-03', 'A-get_connection-04', 'A-get_connection-05'])
def test_get_connection_a(mode, isolated_db):
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
