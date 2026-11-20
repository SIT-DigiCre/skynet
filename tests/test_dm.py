import asyncio

import pytest

import dm


class FakeRole:
    def __init__(self, name):
        self.name = name


class FakeMember:
    def __init__(self, member_id, roles=()):
        self.id = member_id
        self.roles = list(roles)


class FakeGuild:
    def __init__(self, name, members, bot_role):
        self.name = name
        self._members = members
        self._bot_role = bot_role

    def get_role(self, role_id):
        return self._bot_role

    async def fetch_members(self):
        for member in self._members:
            yield member


class FakeClient:
    def __init__(self, guilds):
        self.guilds = guilds


class FakeSettings:
    def __init__(self, active_members_file):
        self.guild_name = "デジクリ"
        self.bot_role_id = 999
        self.obog_role_id = 888
        self.active_members_file = active_members_file


BOT = FakeRole("Bot")


def make_env(tmp_path, active_ids, members):
    list_file = tmp_path / "members.txt"
    list_file.write_text("\n".join(str(i) for i in active_ids) + "\n", encoding="utf-8")
    guild = FakeGuild("デジクリ", members, BOT)
    client = FakeClient([guild])
    return FakeSettings(str(list_file)), client


def test_resolve_targets_purge_list(tmp_path):
    members = [
        FakeMember(1),  # 部員リスト内 -> 対象外
        FakeMember(2, [BOT]),  # Bot -> 対象外
        FakeMember(3),  # 対象
    ]
    settings, client = make_env(tmp_path, [1], members)
    result = asyncio.run(dm.resolve_targets(client, settings, "purge-list"))
    assert [m.id for m in result] == [3]


def test_resolve_targets_all_excludes_only_bot(tmp_path):
    members = [FakeMember(1), FakeMember(2, [BOT]), FakeMember(3)]
    settings, client = make_env(tmp_path, [1], members)
    result = asyncio.run(dm.resolve_targets(client, settings, "all"))
    assert [m.id for m in result] == [1, 3]


def test_resolve_targets_active_only(tmp_path):
    members = [FakeMember(1), FakeMember(2, [BOT]), FakeMember(3)]
    settings, client = make_env(tmp_path, [1, 2], members)
    result = asyncio.run(dm.resolve_targets(client, settings, "active"))
    assert [m.id for m in result] == [1, 2]


def test_load_message_file_reads_utf8(tmp_path):
    path = tmp_path / "note.txt"
    path.write_text("こんにちは\n2行目\n", encoding="utf-8")
    assert dm.load_message_file(str(path)) == "こんにちは\n2行目\n"


def test_load_message_file_missing_raises(tmp_path):
    with pytest.raises(RuntimeError, match="メッセージファイル"):
        dm.load_message_file(str(tmp_path / "nope.txt"))
