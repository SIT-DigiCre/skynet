from dataclasses import dataclass
from pathlib import Path

MESSAGES_DIR = Path(__file__).resolve().parent / "messages"


@dataclass(frozen=True)
class Messages:
    default_dm: str
    obog_dm: str
    kick_reason: str


def _read(name: str) -> str:
    path = MESSAGES_DIR / name
    try:
        return path.read_text(encoding="utf-8")
    except OSError as e:
        raise RuntimeError(f"メッセージファイルを読めません: {path}") from e


def load_messages() -> Messages:
    return Messages(
        default_dm=_read("default_dm.md"),
        obog_dm=_read("obog_dm.md"),
        kick_reason=_read("kick_reason.txt").rstrip("\r\n"),
    )
