# skynet

デジクリ Discord サーバーの部員管理ツール。粛正（未継続部員の削除）と DM の一斉送信を行います。

## セットアップ

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

`.env.example` を `.env` にコピーし、値を設定します。

| キー | 説明 | 例 |
| --- | --- | --- |
| `DISCORD_BOT_TOKEN` | Bot のトークン | （秘密情報。コミットしない） |
| `GUILD_NAME` | 対象ギルド名 | `デジクリ` |
| `OBOG_ROLE_ID` | OB/OG ロールの ID | `756079579768291368` |
| `BOT_ROLE_ID` | Bot ロールの ID | `538012097485864961` |
| `ACTIVE_MEMBERS_FILE` | 現役部員のユーザー ID を1行1件書いたファイル | `members.txt` |

`ACTIVE_MEMBERS_FILE`（`members.txt`）は `.gitignore` 済みで、リポジトリには含まれません。

## 使い方

```powershell
# 対話形式でモードを選ぶ
.\.venv\Scripts\python.exe member-manager.py

# 粛正モード: 削除対象者に DM を送って kick する
.\.venv\Scripts\python.exe member-manager.py purge

# DM 一斉送信モード（kick はしない）
.\.venv\Scripts\python.exe member-manager.py dm --message-file notes.txt --target all

# list モード: 対象ユーザーの一覧表示（DM送信も削除もしない）
.\.venv\Scripts\python.exe member-manager.py list --target purge-list
```

引数で指定しなかった項目は対話で聞かれます。

### purge モード（粛正）

`ACTIVE_MEMBERS_FILE` に無く、Bot ロールを持たないメンバーを削除対象として一覧表示し、`削除しますか？(y/n)` で `y` を入力した場合のみ実行します。対象者には DM を送ってから kick します。DM 送信に失敗しても kick は試行されます。

DM 文面は OBOG ロールの有無で切り替えます（`messages/default_dm.md` / `messages/obog_dm.md`）。kick 理由は `messages/kick_reason.txt` です。いずれも UTF-8 のテキストファイルで、編集すれば次回実行から反映されます。

### dm モード（一斉送信）

送信対象を選んで `--message-file` で指定した UTF-8 テキストファイルの内容そのままを DM で送信します。kick は行いません。送信前に送信対象者を表示し、`送信しますか？(y/n)` で確認します。

| `--target` | 送信対象 |
| --- | --- |
| `purge-list` | 粛正の削除対象者と同じ条件（部員リスト外かつ Bot 以外） |
| `all` | ギルドの全メンバーから Bot 以外 |
| `active` | 現役部員のみ（`ACTIVE_MEMBERS_FILE` の ID） |

### list モード（一覧表示）

`--target` に同じ 3 種類の対象を指定でき、条件に該当するメンバーを `ユーザーID#表示名` で1行ずつ、最後に `対象者数: N` を表示して終了します。DM の送信も kick も行わず、確認プロンプトもありません。dm モードの送信前に、対象が合っているかを確認するのに使えます。

## テスト

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest
```

Discord への実接続を伴う処理（粛正・送信そのもの）はテストしていません。

## 構成

```
member-manager.py    エントリポイント（モードに応じて振り分け）
cli.py               引数解析と対話フォールバック
config.py            .env の読み込みと検証
purge.py             粛正フロー（判定・DM・kick）
dm.py                DM 一斉送信フロー・一覧表示フロー
discord_common.py    ギルド検索・部員リスト読込・対象解決などの共通処理
messages.py          messages/ 配下の文面ファイル読み込み
messages/            DM 文面・kick 理由（UTF-8 テキスト）
tests/               pytest テスト
```

## 注意

- 粛正・一斉送信は取り消せません。実行前に `.env` の設定と対象を必ず確認してください。
- Bot にはサーバーメンバーの kick と DM 送信の権限が必要です。
