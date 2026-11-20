from pathlib import Path

import discord

from config import Settings
from discord_common import create_client, find_guild, load_active_members

TARGETS = {
    "purge-list": "削除対象者と同じ条件（部員リスト外かつBot以外）",
    "all": "全メンバーからBot以外",
    "active": "現役部員のみ（部員リストのID）",
}


def load_message_file(path: str) -> str:
    try:
        return Path(path).read_text(encoding="utf-8")
    except OSError as e:
        raise RuntimeError(f"メッセージファイルを読めません: {path}") from e


async def resolve_targets(
    client: discord.Client,
    settings: Settings,
    target: str,
) -> list[discord.Member]:
    guild = find_guild(client, settings.guild_name)
    active_members = load_active_members(settings.active_members_file)
    bot_role = guild.get_role(settings.bot_role_id)

    members = []
    async for member in guild.fetch_members():
        if target == "all":
            if bot_role not in member.roles:
                members.append(member)
        elif target == "active":
            if member.id in active_members:
                members.append(member)
        else:  # purge-list
            if member.id not in active_members and bot_role not in member.roles:
                members.append(member)
    return members


def create_dm_client(
    settings: Settings, target: str, message: str
) -> discord.Client:
    client = create_client()

    @client.event
    async def on_ready():
        try:
            members = await resolve_targets(client, settings, target)
            for member in members:
                print(f"{member.id}#{member.display_name}")
            print(f"送信対象者数: {len(members)}")
            key = input("送信しますか？(y/n)")
            if key == "y":
                for member in members:
                    try:
                        await member.send(message)
                        print(f"DMを送信しました: {member.id}#{member.display_name}")
                    except discord.Forbidden:
                        print(f"DM送信不可: {member.id}#{member.display_name}")
                    except Exception as e:
                        print(f"DM送信エラー: {member.id} - {e}")
        finally:
            await client.close()

    return client


def run(settings: Settings, target: str, message_file: str) -> None:
    message = load_message_file(message_file)
    client = create_dm_client(settings, target, message)
    client.run(settings.token)
