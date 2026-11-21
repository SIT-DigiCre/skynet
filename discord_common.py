import discord

from config import Settings

TARGETS = {
    "purge-list": "削除対象者と同じ条件（部員リスト外かつBot以外）",
    "all": "全メンバーからBot以外",
    "active": "現役部員のみ（部員リストのID）",
}


def load_active_members(path: str) -> list[int]:
    active_members = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            active_members.append(int(line))
    return active_members


def create_client() -> discord.Client:
    intents = discord.Intents.default()
    # intents.message_content = True
    intents.members = True
    return discord.Client(intents=intents)


def find_guild(client: discord.Client, guild_name: str) -> discord.Guild:
    for guild in client.guilds:
        if guild.name == guild_name:
            return guild
    raise RuntimeError(f"ギルドが見つかりません: {guild_name}")


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
