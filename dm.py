from pathlib import Path

import discord

from config import Settings
from discord_common import create_client, resolve_targets


def load_message_file(path: str) -> str:
    try:
        return Path(path).read_text(encoding="utf-8")
    except OSError as e:
        raise RuntimeError(f"メッセージファイルを読めません: {path}") from e


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


def create_list_client(settings: Settings, target: str) -> discord.Client:
    client = create_client()

    @client.event
    async def on_ready():
        try:
            members = await resolve_targets(client, settings, target)
            for member in members:
                print(f"{member.id}#{member.display_name}")
            print(f"対象者数: {len(members)}")
        finally:
            await client.close()

    return client


def list_targets(settings: Settings, target: str) -> None:
    client = create_list_client(settings, target)
    client.run(settings.token)


def run(settings: Settings, target: str, message_file: str) -> None:
    message = load_message_file(message_file)
    client = create_dm_client(settings, target, message)
    client.run(settings.token)
