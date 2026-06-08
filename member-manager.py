import os
from textwrap import dedent

import discord
from dotenv import load_dotenv

load_dotenv()


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)
active_members = []
with open("members.txt", "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        active_members.append(int(line))

DEFAULT_DM_MSG = dedent("""\
                        # 【デジクリ】退部処理のお知らせ
                        
                        デジクリ インフラ担当です。
                        このDMを受け取ったアカウントは、デジクリサーバーから削除されました。

                        部費を納入したにも関わらず削除された場合には、デジコアに連携されているアカウントが誤っている可能性があります。
                        以下のリンクから再度ご確認をお願いします。
                        https://core3.digicre.net/tutorial/discord

                        なお、こちらのDMは自動送信のため、返信いただいても対応できません。
                        お問い合わせは以下のいずれかよりお願いいたします。

                        インフラサポートチケット: https://forms.gle/a1jWvcvosP6jAdfM9
                        メール: contact@digicre.net
""")

OBOG_DM_MSG = dedent("""\
                        # 【デジクリ】退部処理のお知らせ

                        デジクリ インフラ担当です。
                        このDMはデジクリサーバーに参加されているOB/OGの皆様に送信しています。

                        この度、運営方針の変更に伴い、デジクリサーバーからOB/OGの皆様を削除させていただくことになりました。
                        これまでご参加いただき、ありがとうございました。

                        もしよろしければ、以下のリンクからOB&OGサーバーにご参加いただけますと幸いです。
                        {ここにOB&OGサーバーの招待リンクを挿入}

                        なお、こちらのDMは自動送信のため、返信いただいても対応できません。
                        お問い合わせはメール(contact@digicre.net)よりお願いいたします。
""")


@client.event
async def on_ready():
    delete_members = []
    target_guild: discord.Guild = None
    for guild in client.guilds:
        if guild.name == "デジクリ":
            target_guild = guild
            break
    async for member in target_guild.fetch_members():
        # print(member.name)
        # 既存部員のリストに居ないかつ、OBOGじゃないかつ、Botじゃない人を削除対象者に追加
        if (
            member.id not in active_members
            # and client.guilds[0].get_role(756079579768291368) not in member.roles # OBOG
            and client.guilds[0].get_role(538012097485864961) not in member.roles  # Bot
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
                    DEFAULT_DM_MSG
                    if client.guilds[0].get_role(756079579768291368) not in member.roles
                    else OBOG_DM_MSG
                )
                try:
                    await member.send(dm_message)
                    print(f"DMを送信しました: {member.id}#{member.display_name}")
                except discord.Forbidden:
                    print(f"DM送信不可: {member.id}#{member.display_name}")
                except Exception as e:
                    print(f"DM送信エラー: {member.id} - {e}")
                await member.kick(
                    reason="未継続の部員の削除(継続していて削除された場合はMattermostもしくはメール(contact@digicre.net)にてご相談ください)"
                )
                print(f"{member.id}#{member.display_name}を削除しました")
            except Exception as e:
                print(f"削除エラー: {member.id} - {e}")


client.run(os.getenv("DISCORD_BOT_TOKEN"))
