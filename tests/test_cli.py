import pytest

import cli


def test_parse_purge_args_no_prompts(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda *a: pytest.fail("プロンプトを表示しない"),
    )
    args = cli.parse(["purge"])
    assert args.mode == "purge"
    assert args.target is None
    assert args.message_file is None


def test_parse_dm_full_args(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda *a: pytest.fail("プロンプトを表示しない"),
    )
    args = cli.parse(["dm", "--target", "active", "--message-file", "notes.txt"])
    assert args.mode == "dm"
    assert args.target == "active"
    assert args.message_file == "notes.txt"


def test_parse_interactive_mode_fallback(monkeypatch):
    answers = iter(["1"])
    monkeypatch.setattr("builtins.input", lambda *a: next(answers))
    args = cli.parse([])
    assert args.mode == "purge"


def test_parse_interactive_dm_prompts(monkeypatch):
    answers = iter(["2", "3", "notes.txt"])
    monkeypatch.setattr("builtins.input", lambda *a: next(answers))
    args = cli.parse([])
    assert args.mode == "dm"
    assert args.target == "active"
    assert args.message_file == "notes.txt"


def test_parse_partial_args_only_prompts_missing(monkeypatch):
    # --target は渡したので対象を聞かず、文面パスだけ聞く
    answers = iter(["notes.txt"])
    monkeypatch.setattr("builtins.input", lambda *a: next(answers))
    args = cli.parse(["dm", "--target", "all"])
    assert args.target == "all"
    assert args.message_file == "notes.txt"


def test_parse_invalid_mode_name(monkeypatch):
    answers = iter(["9"])
    monkeypatch.setattr("builtins.input", lambda *a: next(answers))
    with pytest.raises(RuntimeError):
        cli.parse([])


def test_parse_rejects_unknown_mode_via_arg():
    with pytest.raises(SystemExit):
        cli.parse(["bogus"])


def test_parse_empty_message_file_rejected(monkeypatch):
    answers = iter(["2", "1", "  "])
    monkeypatch.setattr("builtins.input", lambda *a: next(answers))
    with pytest.raises(RuntimeError):
        cli.parse([])
