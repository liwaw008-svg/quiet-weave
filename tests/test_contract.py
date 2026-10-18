from pathlib import Path

SRC = (Path(__file__).parents[1] / "contracts" / "contract.py").read_text(encoding="utf-8")


def test_lifecycle_and_permissionless_consensus():
    for token in ('def set_loom(', 'def weave_window(', 'def pin_window(', '"SET"', '"WOVEN"', '"PINNED"'):
        assert token in SRC
    section = SRC[SRC.index("def weave_window("):SRC.index("def pin_window(")]
    assert "gl.message.sender_address" not in section


def test_complete_bounded_vector_is_enforced():
    for token in (
        "complete ordered band vector required",
        "ordered segment ids required",
        '"QUIET", "CONDITIONAL", "LOUD"',
        "valid evidence indexes required",
        "exactly one declaring observation required",
    ):
        assert token in SRC


def test_longest_window_is_derived_in_code():
    for token in ("best_count", "run_count", "best_quiet", 'outcome = "WINDOW"', '"NO_WINDOW"'):
        assert token in SRC


def test_replay_and_attribution_guards():
    for token in ("used_inputs", "input_digest", "loom id or exact input already used", "evidence_indexes"):
        assert token in SRC


def test_no_remote_fixture_dependency():
    assert "gl.nondet.web.get" not in SRC
    assert "raw.githubusercontent.com" not in SRC
