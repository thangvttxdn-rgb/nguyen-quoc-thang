"""Tiện ích chung cho kiểm thử đội Agent: đường dẫn bản mẫu và lệnh git."""

import subprocess
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parents[2]
CONG_CU = GOC / "de-xuat" / "doi-agent-tu-chu" / "cong-cu"
for _p in (CONG_CU, GOC / ".claude" / "hooks"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))


def git(cwd: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True,  # noqa: S603, S607
                          check=check)
