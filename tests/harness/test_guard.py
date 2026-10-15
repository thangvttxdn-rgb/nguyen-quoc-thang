"""Kiểm thử hook .claude/hooks/guard.py."""

import importlib.util
from pathlib import Path

import pytest

GUARD_PATH = Path(__file__).resolve().parents[2] / ".claude" / "hooks" / "guard.py"
spec = importlib.util.spec_from_file_location("guard", GUARD_PATH)
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)

PROJECT = str(Path(__file__).resolve().parents[2])


def bash(command):
    return guard.decide({"tool_name": "Bash", "tool_input": {"command": command}}, PROJECT)


def write(file_path, content):
    payload = {"tool_name": "Write", "tool_input": {"file_path": file_path, "content": content}}
    return guard.decide(payload, PROJECT)


@pytest.mark.parametrize("cmd", [
    "rm -rf build", "rm -fr /", "rm -r -f src", "rm -Rf x", "rm --recursive --force x",
    "sudo rm -rf /", "ls && rm -rf src", "echo hi; rm -r -f .",
])
def test_rm_de_quy_cuong_buc_bi_cam(cmd):
    assert bash(cmd)[0] == "deny"


@pytest.mark.parametrize("cmd", ["rm file.txt", "rm -r build", "rm -f a.log", "grep -rf x ."])
def test_rm_thuong_khong_bi_chan(cmd):
    assert bash(cmd) is None


@pytest.mark.parametrize("cmd", [
    'sqlcmd -S srv -Q "SHUTDOWN WITH NOWAIT"',
    'sqlcmd -Q "DROP DATABASE EMS"',
])
def test_sql_tham_hoa_bi_cam(cmd):
    assert bash(cmd)[0] == "deny"


@pytest.mark.parametrize("cmd", [
    'sqlcmd -Q "DROP TABLE NhanSu"',
    'sqlcmd -Q "ALTER TABLE PhanCong ADD Ghi_chu NVARCHAR(200)"',
    'sqlcmd -Q "DELETE FROM NhanSu WHERE Id = 1"',
    "python -c \"cur.execute('UPDATE NhanSu SET IsActive = 0')\"",
    'sqlcmd -i migration.sql -Q "EXEC sp_CapNhat"',
])
def test_sql_ghi_phai_xin_duyet(cmd):
    assert bash(cmd)[0] == "ask"


@pytest.mark.parametrize("cmd", [
    'sqlcmd -Q "SELECT TOP 10 * FROM NhanSu WITH (NOLOCK)"',
    'grep -rn "DROP TABLE" src/',
    "pytest -q --tb=short",
])
def test_lenh_doc_khong_bi_chan(cmd):
    assert bash(cmd) is None


def test_cam_ghi_ra_ngoai_du_an():
    assert write("/etc/hosts", "x")[0] == "deny"
    assert write("../ngoai.py", "x")[0] == "deny"


@pytest.mark.parametrize("content", [
    'CONN = "DRIVER={ODBC};SERVER=srv;UID=sa;PWD=Abc@123"',
    'DB_PASSWORD = "Abc@123"',
    'cfg = {"password": "Abc@123"}',
    'pyodbc.connect(server, password="Abc@123")',
])
def test_cam_hardcode_mat_khau(content):
    assert write("src/db/connection.py", content)[0] == "deny"


@pytest.mark.parametrize("content", [
    'CONN = f"SERVER={server};UID={user};PWD={password}"',
    'password = os.environ["DB_PASSWORD_READONLY"]',
    "pyodbc.connect(server, password=pwd)",
    'password = ""',
])
def test_mat_khau_tu_bien_moi_truong_hop_le(content):
    assert write("src/db/connection.py", content) is None


def test_file_env_va_tai_lieu_khong_kiem_mat_khau():
    assert write(".env", "DB_PASSWORD_READONLY=Abc@123") is None
    assert write(".env.example", "DB_PASSWORD_READONLY=<điền>") is None
