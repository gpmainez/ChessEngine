import subprocess
import pytest
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ZAD3_SCRIPT = os.path.join(BASE_DIR, "../zad3.py")


def create_test_file(path, lines_count):
    with open(path, "w", encoding="utf-8") as f:
        for i in range(lines_count):
            f.write(f"Linia {i + 1}\n")


def test_tail_basic_file(tmp_path):
    p = tmp_path / "test.txt"
    create_test_file(p, 15)

    result = subprocess.run(['python', ZAD3_SCRIPT, str(p)], capture_output=True, text=True)

    output_lines = result.stdout.strip().split('\n')
    assert len(output_lines) == 10
    assert output_lines[0] == "Linia 6"
    assert output_lines[-1] == "Linia 15"


def test_tail_custom_lines(tmp_path):
    p = tmp_path / "test.txt"
    create_test_file(p, 15)

    result = subprocess.run(['python', ZAD3_SCRIPT, '--lines=3', str(p)], capture_output=True, text=True)

    output_lines = result.stdout.strip().split('\n')
    assert len(output_lines) == 3
    assert output_lines[0] == "Linia 13"


def test_tail_stdin():
    input_data = "1\n2\n3\n4\n5"
    result = subprocess.run(['python', ZAD3_SCRIPT, '--lines=2'], input=input_data, capture_output=True, text=True)

    output_lines = result.stdout.strip().split('\n')
    assert len(output_lines) == 2
    assert output_lines[0] == "4"
    assert output_lines[1] == "5"


def test_tail_file_priority_over_stdin(tmp_path):
    p = tmp_path / "real_file.txt"
    with open(p, "w") as f: f.write("Dane z pliku")

    input_data = "Dane ze stdin"
    result = subprocess.run(['python', ZAD3_SCRIPT, str(p)], input=input_data, capture_output=True, text=True)

    assert "Dane z pliku" in result.stdout

@pytest.mark.parametrize("file_content, lines_arg, expected_count, test_id", [
    ("A\nB\nC\nD\nE", "--lines=2", 2, "Normalny przypadek"),
    ("A\nB", "--lines=10", 2, "Plik krotszy niz n"),
    ("", "--lines=5", 0, "Pusty plik"),
    ("Jedna linia", "--lines=1", 1, "Dokladnie jedna linia"),
    ("1\n2\n3", "--lines=0", 0, "Zero linii"),
])
def test_tail_various_cases(tmp_path, file_content, lines_arg, expected_count, test_id):
    p = tmp_path / f"test_{test_id.replace(' ', '_')}.txt"
    p.write_text(file_content)

    result = subprocess.run(['python', ZAD3_SCRIPT, lines_arg, str(p)], capture_output=True, text=True)

    # Czyscimy wynik i dzielimy na linie
    output = result.stdout.strip()
    output_lines = output.split('\n') if output else []

    # Wiadomość w asercji wyświetli się przy błędzie (FAILED)
    assert len(output_lines) == expected_count, \
        f"FAILED w '{test_id}': Oczekiwano {expected_count} linii, a otrzymano {len(output_lines)}. Wyjście: {output}"

    print(f"OK: {test_id} przeszło pomyślnie!")


def test_tail_invalid_file():
    # Testujemy co się stanie jak plik nie istnieje
    result = subprocess.run(['python', ZAD3_SCRIPT, "nie_ma_mnie.txt"], capture_output=True, text=True)
    # Twój kod prawdopodobnie rzuci FileNotFoundError - sprawdźmy czy program nie wybuchł fatalnie
    assert result.returncode != 0 or "Error" in result.stderr, "FAILED: Program powinien zgłosić błąd dla nieistniejącego pliku"
