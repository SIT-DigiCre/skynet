import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    token: str
    guild_name: str
    obog_role_id: int
    bot_role_id: int
    active_members_file: str


def _require(name: str) -> str:
    value = os.getenv(name)
    if value is None or not value.strip():
        raise RuntimeError(f"{name} が .env に設定されていません")
    return value.strip()


def _require_int(name: str) -> int:
    value = _require(name)
    try:
        return int(value)
    except ValueError as e:
        raise RuntimeError(f"{name} は整数である必要があります: {value}") from e


def load_settings() -> Settings:
    return Settings(
        token=_require("DISCORD_BOT_TOKEN"),
        guild_name=_require("GUILD_NAME"),
        obog_role_id=_require_int("OBOG_ROLE_ID"),
        bot_role_id=_require_int("BOT_ROLE_ID"),
        active_members_file=_require("ACTIVE_MEMBERS_FILE"),
    )
