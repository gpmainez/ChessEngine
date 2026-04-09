import subprocess
import os
import pytest

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ZAD4_SCRIPT = os.path.join(BASE_DIR, "../zad4.py")


def test_zad4_empty_directory(tmp_path):
    """Przypadek 1: Folder istnieje, ale jest pusty."""
    empty_dir = tmp_path / "pusty_folder"
    empty_dir.mkdir()

    result = subprocess.run(['python', ZAD4_SCRIPT, str(empty_dir)], capture_output=True, text=True)

    assert "could not analize" in result.stdout.lower() or "0" in result.stdout
    print("OK: Pusty folder obsłużony.")


def test_zad4_math_accuracy(tmp_path):
    """Przypadek 2: Sprawdzenie matematyki."""
    d = tmp_path / "math_test"
    d.mkdir()
    (d / "f1.txt").write_text("raz dwa", encoding="utf-8")
    (d / "f2.txt").write_text("trzy\ncztery", encoding="utf-8")

    result = subprocess.run(['python', ZAD4_SCRIPT, str(d)], capture_output=True, text=True, encoding="utf-8")
    output = result.stdout

    assert "4" in output
    assert "3" in output
    print("OK: Matematyka się zgadza.")


def test_zad4_non_existent_directory():
    """Przypadek 4: Folder nie istnieje."""
    result = subprocess.run(['python', ZAD4_SCRIPT, "sciezka_ktorej_nie_ma_12345"], capture_output=True, text=True)

    assert "not a catalogue" in result.stdout.lower()
    assert result.returncode != 0
    print("OK: Walidacja braku folderu działa.")


@pytest.mark.parametrize("content, expected_winner", [
    ("aaa bbb bbb", "bbb"),
    ("word1 word1 word2", "word1"),
])
def test_zad4_global_winner_logic(tmp_path, content, expected_winner):
    """Przypadek 5: Zwycięzca globalny."""
    d = tmp_path / f"winner_test_{expected_winner}"
    d.mkdir()
    (d / "file.txt").write_text(content, encoding="utf-8")

    result = subprocess.run(['python', ZAD4_SCRIPT, str(d)], capture_output=True, text=True, encoding="utf-8")

    assert expected_winner in result.stdout
    print(f"OK: Zwycięzca '{expected_winner}' wyłoniony.")