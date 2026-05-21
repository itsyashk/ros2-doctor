from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class CheckStatus(str, Enum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"
    SKIP = "skip"
    INFO = "info"


@dataclass
class CheckResult:
    id: str
    title: str
    status: CheckStatus
    message: str = ""
    fix_command: str = ""
    evidence: str = ""
    category: str = "general"


@dataclass
class CheckSummary:
    results: list[CheckResult] = field(default_factory=list)

    def counts(self) -> tuple[int, int, int, int]:
        passed = warned = failed = skipped = 0
        for r in self.results:
            if r.status == CheckStatus.PASS:
                passed += 1
            elif r.status == CheckStatus.WARN:
                warned += 1
            elif r.status == CheckStatus.FAIL:
                failed += 1
            elif r.status == CheckStatus.SKIP:
                skipped += 1
        return passed, warned, failed, skipped

    def fix_commands(self) -> list[str]:
        seen: set[str] = set()
        cmds: list[str] = []
        for r in self.results:
            if r.fix_command and r.fix_command not in seen:
                seen.add(r.fix_command)
                cmds.append(r.fix_command)
        return cmds
