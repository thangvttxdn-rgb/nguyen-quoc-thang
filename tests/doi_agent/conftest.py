"""Kiểm thử bản mẫu đội Agent - không gọi model, không tốn token."""

from pathlib import Path

import pytest
from tien_ich_doi_agent import git


@pytest.fixture
def kho(tmp_path: Path) -> Path:
    """Kho git tạm có nhánh main và 3 tệp - đóng vai mã nguồn gốc."""
    goc = tmp_path / "kho"
    goc.mkdir()
    git(goc, "init", "-q", "-b", "main")
    git(goc, "config", "user.email", "kiem-thu@vi-du.invalid")
    git(goc, "config", "user.name", "Kiem thu")
    for ten in ("a.py", "b.py", "c.py"):
        (goc / ten).write_text(f"GIA_TRI = '{ten}'\n", encoding="utf-8")
    git(goc, "add", ".")
    git(goc, "commit", "-q", "-m", "goc")
    return goc
