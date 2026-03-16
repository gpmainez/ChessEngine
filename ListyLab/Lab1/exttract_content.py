import sys
import io
from uni_fun import clean, read_stream

sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def extract():
    start_book = False
    previous_line_empty = False
    buffer = ""
    early_buffer = ""
    line_count = 0
    cleaned = ""

    for char in read_stream():
        if char == "\n":
            line_count += 1
            cleaned = clean(buffer)

            if cleaned[:5] == "-----":
                break

            formatted_line = cleaned + "\n" if cleaned != "" else "\n"

            if not start_book:
                early_buffer += formatted_line

                if cleaned == "" and previous_line_empty:
                    start_book = True
                    early_buffer = ""
                elif line_count >= 10:
                    start_book = True
                    yield early_buffer
                    early_buffer = ""

                previous_line_empty = (cleaned == "")
            else:
                yield formatted_line

            buffer = ""
        else:
            buffer += char

    if buffer != "":
        cleaned = clean(buffer)
    if not start_book:
        yield early_buffer + cleaned + "\n"
    else:
        yield cleaned + "\n"


def main():
    for line in extract():
        sys.stdout.write(line)


if __name__ == "__main__":
    main()
