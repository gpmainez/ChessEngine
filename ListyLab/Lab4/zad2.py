import os
import argparse

def get_path_dirs(path_str):

    dirs = path_str.split(os.pathsep)
    seen = set()
    valid_dirs = []
    
    for d in dirs:
        if d and d not in seen and os.path.isdir(d):
            seen.add(d)
            valid_dirs.append(d)
            
    return valid_dirs

def is_executable(filepath, os_name=os.name):

    if not os.path.isfile(filepath):
        return False
        
    if os_name == 'nt':
        valid_extensions = {'.exe', '.bat', '.cmd'}
        _, ext = os.path.splitext(filepath)
        return ext.lower() in valid_extensions
    else:
        return os.access(filepath, os.X_OK)

def get_executables(dirpath, os_name=os.name):

    executables = []
    try:
        for filename in os.listdir(dirpath):
            filepath = os.path.join(dirpath, filename)
            if is_executable(filepath, os_name):
                executables.append(filename)
    except PermissionError:
        pass
        
    return sorted(executables)

def main():
    parser = argparse.ArgumentParser(description="Eksplorator zmiennej srodowiskowej PATH.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--dirs', action='store_true', help='Wypisz katalogi ze zmiennej PATH')
    group.add_argument('--exe', action='store_true', help='Wypisz katalogi wraz z plikami wykonywalnymi')
    
    args = parser.parse_args()
    
    system_path = os.environ.get('PATH', '')
    dirs = get_path_dirs(system_path)
    
    if args.dirs:
        for d in dirs:
            print(d)
            
    elif args.exe:
        for d in dirs:
            print(f"\n[{d}]")
            executables = get_executables(d)
            if executables:
                for exe in executables:
                    print(f"  - {exe}")
            else:
                print("  (brak dostepnych plkikow wykonywalnych)")

if __name__ == "__main__":
    main()