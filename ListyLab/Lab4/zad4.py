import sys
import os
import subprocess
import csv
import io
from collections import Counter


def main():
    if len(sys.argv) < 2:
        print("Użycie: python zad4and5.py <sciezka_do_katalogu>")
        sys.exit(1)

    directory = sys.argv[1]

    if not os.path.isdir(directory):
        print(f"err: '{directory}' not a catalogue.")
        sys.exit(1)

    results = []

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)

        if not os.path.isfile(filepath):
            continue

        try:

            JAVA_OUT_DIR =r"C:\Users\pc\IdeaProjects\first\src"
            process = subprocess.Popen(
                ['java','-cp',JAVA_OUT_DIR, 'Paradygmaty.streamFun.statistics'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8'
            )

            stdout, stderr = process.communicate(input=filepath)

            if stderr:
                print(f"java catch err {filepath}: {stderr.strip()}")

            if stdout.strip():
                csv_reader = csv.DictReader(io.StringIO(stdout.strip()))
                for row in csv_reader:
                    results.append(row)

        except Exception as e:
            print(f"java compile err {filepath}: {e}")


    if not results:
        print("could not analize")
        return

    total_files = len(results)
    total_chars = sum(int(row['chars']) for row in results)
    total_words = sum(int(row['words']) for row in results)
    total_lines = sum(int(row['lines']) for row in results)

    #gloablny zwyciezca z wielu plikow
    global_top_char = Counter(row['top_char'] for row in results).most_common(1)[0][0]
    global_top_word = Counter(row['top_word'] for row in results).most_common(1)[0][0]


    print("\n" + "=" * 40)
    print("        GLOBALNE STATYSTYKI")
    print("=" * 40)
    print(f"Liczba przeczytanych plików: {total_files}")
    print(f"Sumaryczna liczba znaków:    {total_chars}")
    print(f"Sumaryczna liczba słów:      {total_words}")
    print(f"Sumaryczna liczba wierszy:   {total_lines}")
    print(f"Znak występujący najczęściej: '{global_top_char}'")
    print(f"Słowo występujące najczęściej: '{global_top_word}'")
    print("=" * 40)


if __name__ == "__main__":
    main()