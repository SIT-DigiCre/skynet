import pytest

import discord_common


def test_load_active_members_skips_blank_lines(tmp_path):
    path = tmp_path / "members.txt"
    path.write_text("1\n\n  2  \n\n3\n", encoding="utf-8")
    assert discord_common.load_active_members(str(path)) == [1, 2, 3]


def test_load_active_members_empty_file(tmp_path):
    path = tmp_path / "members.txt"
    path.write_text("", encoding="utf-8")
    assert discord_common.load_active_members(str(path)) == []


def test_find_guild_returns_match():
    client = type("C", (), {"guilds": [FakeGuild("他"), FakeGuild("デジクリ")]})()
    assert discord_common.find_guild(client, "デジクリ").name == "デジクリ"


def test_find_guild_missing_raises():
    client = type("C", (), {"guilds": [FakeGuild("他")]})()
    with pytest.raises(RuntimeError, match="デジクリ"):
        discord_common.find_guild(client, "デジクリ")


class FakeGuild:
    def __init__(self, name):
        self.name = name
