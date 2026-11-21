import argparse

from discord_common import TARGETS

MODES = {
    "purge": "粛正（DM送信 + 部員削除）",
    "dm": "DMの一斉送信（削除なし）",
    "list": "対象ユーザーの一覧表示（DM送信も削除もしない）",
}


def _ask_mode() -> str:
    print("モードを選択してください:")
    keys = list(MODES)
    for i, key in enumerate(keys, start=1):
        print(f"  {i}. {key}: {MODES[key]}")
    answer = input(f"モード [1-{len(keys)}]: ")
    if answer.isdigit() and 1 <= int(answer) <= len(keys):
        answer = keys[int(answer) - 1]
    if answer not in MODES:
        raise RuntimeError(f"未知のモードです: {answer}")
    return answer


def _ask_target() -> str:
    print("対象を選択してください:")
    keys = list(TARGETS)
    for i, key in enumerate(keys, start=1):
        print(f"  {i}. {key}: {TARGETS[key]}")
    answer = input("対象 [1-3]: ")
    if answer.isdigit() and 1 <= int(answer) <= len(keys):
        answer = keys[int(answer) - 1]
    if answer not in TARGETS:
        raise RuntimeError(f"未知の対象です: {answer}")
    return answer


def _ask_message_file() -> str:
    path = input("メッセージファイルのパス: ").strip()
    if not path:
        raise RuntimeError("メッセージファイルのパスを入力してください")
    return path


def parse(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="デジクリ Discord 部員管理ツール")
    parser.add_argument(
        "mode",
        nargs="?",
        choices=list(MODES),
        help="動作モード（省略時は対話で選択）",
    )
    parser.add_argument(
        "--target",
        choices=list(TARGETS),
        help="dm/listモードの対象（省略時は対話で選択）",
    )
    parser.add_argument(
        "--message-file",
        help="dmモードで送るメッセージファイルのパス（省略時は対話で入力）",
    )
    args = parser.parse_args(argv)

    if args.mode is None:
        args.mode = _ask_mode()
    if args.mode in ("dm", "list") and args.target is None:
        args.target = _ask_target()
    if args.mode == "dm" and args.message_file is None:
        args.message_file = _ask_message_file()
    return args
