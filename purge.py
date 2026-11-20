import discord

from config import Settings
from messages import Messages


def load_active_members(path: str) -> list[int]:
    active_members = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            active_members.append(int(line))
    return active_members


def create_client(settings: Settings, messages: Messages) -> discord.Client:
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    client = discord.Client(intents=intents)
    active_members = load_active_members(settings.active_members_file)

    @client.event
    async def on_ready():
        delete_members = []
        target_guild: discord.Guild = None
        for guild in client.guilds:
            if guild.name == settings.guild_name:
                target_guild = guild
                break
        async for member in target_guild.fetch_members():
            # print(member.name)
            # 既存部員のリストに居ないかつ、OBOGじゃないかつ、Botじゃない人を削除対象者に追加
            if (
                member.id not in active_members
                # and client.guilds[0].get_role(settings.obog_role_id) not in member.roles # OBOG
                and client.guilds[0].get_role(settings.bot_role_id) not in member.roles  # Bot
            ):
                delete_members.append(member)
        for member in delete_members:
            print(f"{member.id}#{member.display_name}")
        print(f"削除対象者数: {len(delete_members)}")
        key = input("削除しますか？(y/n)")
        if key == "y":
            for member in delete_members:
                try:
                    dm_message = (
                        messages.default_dm
                        if client.guilds[0].get_role(settings.obog_role_id)
                        not in member.roles
                        else messages.obog_dm
                    )
                    try:
                        await member.send(dm_message)
                        print(f"DMを送信しました: {member.id}#{member.display_name}")
                    except discord.Forbidden:
                        print(f"DM送信不可: {member.id}#{member.display_name}")
                    except Exception as e:
                        print(f"DM送信エラー: {member.id} - {e}")
                    await member.kick(reason=messages.kick_reason)
                    print(f"{member.id}#{member.display_name}を削除しました")
                except Exception as e:
                    print(f"削除エラー: {member.id} - {e}")

    return client


def run(settings: Settings, messages: Messages) -> None:
    client = create_client(settings, messages)
    client.run(settings.token)
