import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connected")
    except Error as e:
        print(e)
    return conn


def execute_sql(cur, sql):
    """ Execute sql
    :param conn: Connection object
    :param sql: a SQL script
    :return:
    """
    try:
        cur.execute(sql)
    except Error as e:
        print(e)

def select_where(conn, table, **query):
    """
    Query tasks from table with data from **query dict
    :param conn: the Connection object
    :param table: table name
    :param query: dict of attributes and values
    :return:
    """

    cur = conn.cursor()
    qs = []
    values = ()
    for k, v in query.items():
        qs.append(f"{k}=?")
        values += (v,)
    q = " AND ".join(qs)
    cur.execute(f"SELECT * FROM {table} WHERE {q}", values)
    rows = cur.fetchall()
    return rows

def delete_where(conn, table, **kwargs):
   """
   Delete from table where attributes from
   :param conn:  Connection to the SQLite database
   :param table: table name
   :param kwargs: dict of attributes and values
   :return:
   """
   qs = []
   values = tuple()
   for k, v in kwargs.items():
       qs.append(f"{k}=?")
       values += (v,)
   q = " AND ".join(qs)

   sql = f'DELETE FROM {table} WHERE {q}'
   cur = conn.cursor()
   cur.execute(sql, values)
   conn.commit()

def update(conn, table, id, query):
    """
    update status, begin_date, and end date of a task
    :param conn:
    :param table: table name
    :param id: row id
    :return:
    """
    parameters = [f"{k} = ?" for k in query]
    parameters = ", ".join(parameters)
    values = tuple(v for v in query.values())
    values += (id, )

    sql = f''' UPDATE {table}
                SET {parameters}
                WHERE id = ?'''
    try:
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
    except sqlite3.OperationalError as e:
        print(e)


class TodosSQLite():
    def __init__(self, db_file):
        self.db_file = db_file

    def create(self):
        create_task_sql = """
        -- projects table
        CREATE TABLE IF NOT EXISTS tasks (
            id integer PRIMARY KEY,
            title text,
            description text,
            status text
        );
        """
        conn = create_connection(self.db_file)
        if conn is not None:
            cur = conn.cursor()
            execute_sql(cur, create_task_sql)
            conn.close()
    
    def show(self):
        sql = "SELECT * FROM tasks"
        conn = create_connection(self.db_file)
        if conn is not None:
            cur = conn.cursor()
            execute_sql(cur, sql)
            rows = cur.fetchall()
            conn.close()
            return rows

    def add_task(self, data):
        sql = '''INSERT INTO tasks(title, description, status)
             VALUES(?,?,?)'''
        task = tuple(v for v in data.values())[0:3]
        conn = create_connection(self.db_file)
        if conn is not None:
            cur = conn.cursor()
            cur.execute(sql, task)
            conn.commit()
            task_id = cur.lastrowid
            conn.close()
            return task_id


    def get(self, todo_id):
        conn = create_connection(self.db_file)
        if conn is not None:
            todo = select_where(conn, "tasks", id=todo_id)
            conn.close()
            return todo

    def update(self, todo_id, data):
        conn = create_connection(self.db_file)
        if conn is not None:
            query = { key:value for key,value in data.items() if key != 'csrf_token'}
            update(conn, "tasks", todo_id, query)
            conn.close()

    def delete(self, todo_id):
        conn = create_connection(self.db_file)
        if conn is not None:
            delete_where(conn, "tasks", id=todo_id)
            conn.close()



todos_sqlite = TodosSQLite('todos.db')