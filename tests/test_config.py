import pytest

import config

ALL_KEYS = [
    "DISCORD_BOT_TOKEN",
    "GUILD_NAME",
    "OBOG_ROLE_ID",
    "BOT_ROLE_ID",
    "ACTIVE_MEMBERS_FILE",
]


@pytest.fixture
def clean_env(monkeypatch):
    for key in ALL_KEYS:
        monkeypatch.delenv(key, raising=False)
    return monkeypatch


def set_all(monkeypatch, **overrides):
    values = {
        "DISCORD_BOT_TOKEN": "token",
        "GUILD_NAME": "デジクリ",
        "OBOG_ROLE_ID": "756079579768291368",
        "BOT_ROLE_ID": "538012097485864961",
        "ACTIVE_MEMBERS_FILE": "members.txt",
    }
    values.update(overrides)
    for key, value in values.items():
        monkeypatch.setenv(key, value)


def test_load_settings_ok(clean_env):
    set_all(clean_env)
    settings = config.load_settings()
    assert settings.token == "token"
    assert settings.guild_name == "デジクリ"
    assert settings.obog_role_id == 756079579768291368
    assert settings.bot_role_id == 538012097485864961
    assert settings.active_members_file == "members.txt"


@pytest.mark.parametrize("missing", ALL_KEYS)
def test_missing_key_raises(clean_env, missing):
    set_all(clean_env)
    clean_env.delenv(missing)
    with pytest.raises(RuntimeError, match=missing):
        config.load_settings()


@pytest.mark.parametrize("blank", ["", "   "])
def test_blank_value_raises(clean_env, blank):
    set_all(clean_env, GUILD_NAME=blank)
    with pytest.raises(RuntimeError, match="GUILD_NAME"):
        config.load_settings()


def test_non_integer_role_id_raises(clean_env):
    set_all(clean_env, OBOG_ROLE_ID="not-a-number")
    with pytest.raises(RuntimeError, match="OBOG_ROLE_ID"):
        config.load_settings()
