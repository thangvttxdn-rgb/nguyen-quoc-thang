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


# --- HyperFrames (kỹ năng video) ---

@pytest.mark.parametrize("cmd", [
    "npx hyperframes render",                      # không ghim
    "npx hyperframes@latest render",
    "npx -y hyperframes@0.9.36 init demo",
    "npx hyperframes@0.9.37 events --skill=hyperframes",
    "npx hyperframes@0.9.37 feedback --rating 5",
    "npx hyperframes@0.9.37 auth login",
    "npx hyperframes@0.9.37 usage --json",
    "npx hyperframes@0.9.37 publish",
    "npx hyperframes@0.9.37 lambda deploy",
    "npx hyperframes@0.9.37 capture https://example.com",
    "npx hyperframes@0.9.37 telemetry enable",
    "cd video/demo && npx hyperframes@0.9.37 share",
    "HYPERFRAMES_NO_TELEMETRY=0 npx hyperframes@0.9.37 events",
])
def test_hyperframes_bi_cam(cmd):
    assert bash(cmd)[0] == "deny"


@pytest.mark.parametrize("cmd", [
    "npx hyperframes@0.9.37 browser ensure",
    "npx hyperframes@0.9.37 upgrade",
    "npx hyperframes@0.9.37 add orbit-card --on-device",
])
def test_hyperframes_tai_them_phai_hoi(cmd):
    assert bash(cmd)[0] == "ask"


@pytest.mark.parametrize("cmd", [
    "npx hyperframes@0.9.37 render --output renders/a.mp4",
    "HYPERFRAMES_NO_TELEMETRY=1 npx -y hyperframes@0.9.37 init video/demo",
    "npx hyperframes@0.9.37 telemetry disable",
    "npx hyperframes@0.9.37 --version",
    "grep -rn 'npx hyperframes events' .claude/skills",   # chỉ tìm chữ, không chạy
    "git commit -m 'ghim npx hyperframes render'",
])
def test_hyperframes_duoc_phep(cmd):
    assert bash(cmd) is None
