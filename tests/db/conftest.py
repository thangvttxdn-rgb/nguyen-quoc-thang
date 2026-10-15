"""Kết nối giả có kịch bản: mỗi lần execute lấy kết quả kế tiếp trong hàng đợi."""

import pytest


class ScriptedCursor:
    def __init__(self, conn):
        self.conn, self.rowcount, self.description, self._rows = conn, -1, None, []

    def execute(self, sql, *params):
        self.conn.executed.append((sql, params))
        rowcount, columns, rows = self.conn.results.pop(0)
        self.rowcount, self._rows = rowcount, rows
        self.description = [(c,) for c in columns]

    def fetchall(self):
        return self._rows

    def close(self):
        pass


class ScriptedConn:
    def __init__(self):
        self.results, self.executed = [], []
        self.commits = self.rollbacks = 0

    def will_return(self, rowcount=-1, columns=(), rows=()):
        self.results.append((rowcount, list(columns), list(rows)))
        return self

    def cursor(self):
        return ScriptedCursor(self)

    def commit(self):
        self.commits += 1

    def rollback(self):
        self.rollbacks += 1


@pytest.fixture
def conn():
    return ScriptedConn()
