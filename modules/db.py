"""Database wrapper extracted from original SQL class."""
import pymysql
from typing import Any
from . import config


class SQL:
    def __init__(self, debug: bool = True):
        self.host = config.MYSQL['host']
        self.user = config.MYSQL['user']
        self.port = config.MYSQL['port']
        self.password = config.MYSQL['password']
        self.charset = config.MYSQL['charset']
        self.db = config.MYSQL['db']
        self.conn = None
        self.cursor = None
        self.debug = debug

    def connect(self) -> Any:
        try:
            self.conn = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                db=self.db,
                charset=self.charset
            )
            self.cursor = self.conn.cursor()
            return 1
        except Exception as e:
            return e

    def _exec_fetchall(self, sql: str):
        if self.debug:
            print("SQL exec:", sql)
        try:
            self.conn.ping(reconnect=True)
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Exception as e:
            return e

    def search(self, table: str, condition: str):
        sql = f"SELECT * FROM {table} WHERE {condition}"
        return self._exec_fetchall(sql)

    def delete(self, table: str, condition: str):
        try:
            self.conn.ping(reconnect=True)
            self.cursor.execute(f"DELETE FROM {table} WHERE {condition}")
            self.conn.commit()
            return 1
        except Exception as e:
            return e

    def add(self, table: str, wv: str, vv: str):
        try:
            self.conn.ping(reconnect=True)
            self.cursor.execute(f"INSERT INTO {table}({wv}) VALUES ({vv})")
            self.conn.commit()
            return 1
        except Exception as e:
            return e

    def update(self, table: str, uv: str, vv: str, condition: str):
        try:
            self.conn.ping(reconnect=True)
            sql = f"UPDATE {table} SET {uv}={vv} WHERE {condition}"
            if self.debug:
                print("[SQL] update exec:", sql)
            self.cursor.execute(sql)
            self.conn.commit()
            return 1
        except Exception as e:
            return e

    def advance_select(self, wv: str, table: str, condition: str):
        try:
            self.conn.ping(reconnect=True)
            sql = f"select {wv} from {table} where {condition}"
            self.cursor.execute(sql)
            if self.debug:
                print("SQL exec:", sql)
            return self.cursor.fetchall()
        except Exception as e:
            return e
