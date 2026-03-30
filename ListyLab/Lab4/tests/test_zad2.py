import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, ".."))

from zad2 import get_path_dirs, is_executable, get_executables

def test_get_path_dirs(tmp_path):

    d1 = tmp_path / "dir1"
    d2 = tmp_path / "dir2"
    d1.mkdir()
    d2.mkdir()
    

    fake_path = f"{d1}{os.pathsep}{d2}{os.pathsep}fake_dir_6767"
    

    result = get_path_dirs(fake_path)
    
    assert str(d1) in result
    assert str(d2) in result
    assert "fake_dir_6767" not in result

def test_is_executable_windows(tmp_path):

    p_exe = tmp_path / "script.exe"
    p_txt = tmp_path / "text.txt"
    p_exe.write_text("bartek")
    p_txt.write_text("adriaan")
    
    assert is_executable(str(p_exe), os_name='nt') is True
    assert is_executable(str(p_txt), os_name='nt') is False

def test_get_executables(tmp_path):

    (tmp_path / "app.exe").write_text("adr")
    (tmp_path / "run.bat").write_text("ian")
    (tmp_path / "readme.md").write_text("ola")
    
    result = get_executables(str(tmp_path), os_name='nt')
    
    assert "app.exe" in result
    assert "run.bat" in result
    assert "readme.md" not in result
    assert len(result) == 2