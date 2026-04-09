import os
import argparse
import subprocess
from datetime import datetime
import utils

IMAGE_EXTENSIONS = {'.jpeg', '.jpg', '.png','.gif', '.bmp', '.webp'}
MEDIA_EXTENSIONS = {'.mp3', '.mp4', '.mkv', '.avi', '.wav', '.flac', '.webm'}

def process_file(input_path, target_format):
    _, ext = os.path.splitext(input_path)
    ext = ext.lower()
    
    if ext in IMAGE_EXTENSIONS:
        tool = 'magick'
    elif ext in MEDIA_EXTENSIONS:
        tool = 'ffmpeg'
    else:
        print(f"Nieznany format pliku, pomijamy: {input_path}")
        return

    out_dir = utils.get_converted_dir()
    filename = os.path.basename(input_path)
    name_without_ext, _ = os.path.splitext(filename)
    

    timestamp = utils.get_timestamp_string()
    out_filename = f"{timestamp}-{name_without_ext}.{target_format}"
    out_path = os.path.join(out_dir, out_filename)
    

    if tool == 'ffmpeg':
        cmd = ['ffmpeg', '-y', '-i', input_path, out_path] # -y nadpisuje bez osrzezemoa a -i to input
    else:
        cmd = ['magick', input_path, out_path]
        
    print(f"Konwersja: {input_path} ---> {out_path} [{tool}]")
    
    try:

        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "original_path": input_path,
            "target_format": target_format,
            "output_path": out_path,
            "tool_used": tool
        }
        utils.save_history(out_dir, record)
        print("Zakończono sukcesem.")
        
    except subprocess.CalledProcessError:
        print(f"Blad podczas konwersji pliku {input_path}. Proces {tool} zwrocil blad")
    except FileNotFoundError:
        print(f"Nie znaleziono {tool}!!!")

def main():
    parser = argparse.ArgumentParser(description="Konwerter plików multimedialnych i obrazow.")
    parser.add_argument('input_dir', help="Sciezka do katalogu z plikami zrodlowymi")
    parser.add_argument('--format', required=True, help="Docelowy format pliku (np. png, webm, mp3)")
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.input_dir):
        print(f"Blad: Ścieżka '{args.input_dir}' nie jest katalogiem.")
        return
        
    for filename in os.listdir(args.input_dir):
        filepath = os.path.join(args.input_dir, filename)
        if os.path.isfile(filepath):
            process_file(filepath, args.format)

if __name__ == "__main__":
    main()