import psycopg2
from adapters.db.sqlite_adapter import SQLiteAdapter

class PostgresAdapter(SQLiteAdapter):
    def __init__(self, dsn: str):
        self.conn = psycopg2.connect(dsn)
        self.conn.autocommit = True
        self._init_schema()
    def _init_schema(self):
        with self.conn.cursor() as cur:
            cur.execute('''CREATE TABLE IF NOT EXISTS character (id TEXT PRIMARY KEY, name TEXT, level INTEGER, exp INTEGER, profession TEXT);''')