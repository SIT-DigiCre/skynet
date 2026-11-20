import discord


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
    intents.message_content = True
    intents.members = True
    return discord.Client(intents=intents)


def find_guild(client: discord.Client, guild_name: str) -> discord.Guild:
    for guild in client.guilds:
        if guild.name == guild_name:
            return guild
    raise RuntimeError(f"ギルドが見つかりません: {guild_name}")
