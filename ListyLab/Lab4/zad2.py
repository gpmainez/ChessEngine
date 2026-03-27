import os
import argparse

def get_path_dirs():

    path_str = os.environ.get('PATH', '')
    dirs = path_str.split(os.pathsep)
    
    seen = set()
    valid_dirs = []
    for d in dirs:
        if d and d not in seen and os.path.isdir(d): #ddodajemy katalogi ktore nie sa puste nie widzielismy ich jeszcze i rzeczywiscie istnieja
            seen.add(d)
            valid_dirs.append(d)
            
    return valid_dirs

def is_executable(filepath):

    if not os.path.isfile(filepath):
        return False
        
    if os.name == 'nt':
        valid_extensions = {'.exe', '.bat', '.cmd'}
        _, ext = os.path.splitext(filepath)
        return ext.lower() in valid_extensions
    else:
        return os.access(filepath, os.X_OK)

def get_executables(dirpath):

    executables = []
    try:
        for filename in os.listdir(dirpath):
            filepath = os.path.join(dirpath, filename)
            if is_executable(filepath):
                executables.append(filename)
    except PermissionError:
        pass
        
    return sorted(executables)

def main():
    pass

if __name__ == "__main__":
    main()