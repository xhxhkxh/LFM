"""Database wrapper implemented with SQLAlchemy Core."""
from typing import Any, Optional, List, Tuple

# Support both package imports (preferred) and direct script execution for
# quick debugging. When running as a module (recommended) the relative import
# works; when executing the file directly, fall back to absolute import.
try:
    from . import config
except Exception:
    # running as script: ensure package import works
    import modules.config as config
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine, Result

# runtime-assigned DB instance (set by app factory)
sql: Optional["SQL"] = None


class SQL:
    def __init__(self, debug: bool = True):
        mysql = config.MYSQL
        # 使用 SQLAlchemy engine，驱动使用 PyMySQL（确保 requirements 中有 PyMySQL）
        self.url = f"mysql+pymysql://{mysql['user']}:{mysql['password']}@{mysql['host']}:{mysql['port']}/{mysql['db']}?charset={mysql.get('charset', 'utf8mb4')}"
        self.engine: Optional[Engine] = None
        self.debug = debug

    def connect(self) -> Any:
        try:
            self.engine = create_engine(
                self.url, echo=self.debug, pool_pre_ping=True)
            # simple test connection
            with self.engine.connect() as conn:
                conn.execute(text('SELECT 1'))
            return 1
        except Exception as e:
            # Common cause: missing cryptography package required by
            # sha256_password / caching_sha2_password authentication.
            msg = str(e)
            if 'sha256_password' in msg or 'caching_sha2_password' in msg or 'cryptography' in msg:
                return RuntimeError("DB connect failed: cryptography package is required for sha256_password or caching_sha2_password auth methods. Please `pip install cryptography` and try again. Original error: {}".format(msg))
            return e

    def _exec_fetchall(self, sql_statement: str) -> Any:
        if self.debug:
            print('SQL exec:', sql_statement)
        try:
            with self.engine.connect() as conn:
                res: Result = conn.execute(text(sql_statement))
                return [tuple(r) for r in res.fetchall()]
        except Exception as e:
            return e

    def search(self, table: str, condition: str) -> Any:
        sql_statement = f"SELECT * FROM {table} WHERE {condition}"
        return self._exec_fetchall(sql_statement)

    def delete(self, table: str, condition: str) -> Any:
        try:
            sql_statement = f"DELETE FROM {table} WHERE {condition}"
            with self.engine.begin() as conn:
                conn.execute(text(sql_statement))
            return 1
        except Exception as e:
            return e

    def add(self, table: str, wv: str, vv: str) -> Any:
        try:
            sql_statement = f"INSERT INTO {table}({wv}) VALUES ({vv})"
            with self.engine.begin() as conn:
                conn.execute(text(sql_statement))
            return 1
        except Exception as e:
            return e

    def update(self, table: str, uv: str, vv: str, condition: str) -> Any:
        try:
            sql_statement = f"UPDATE {table} SET {uv}={vv} WHERE {condition}"
            if self.debug:
                print('[SQL] update exec:', sql_statement)
            with self.engine.begin() as conn:
                conn.execute(text(sql_statement))
            return 1
        except Exception as e:
            return e

    def advance_select(self, wv: str, table: str, condition: str) -> Any:
        try:
            sql_statement = f"SELECT {wv} FROM {table} WHERE {condition}"
            return self._exec_fetchall(sql_statement)
        except Exception as e:
            return e
