import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, ".."))

from zad1 import filter_env_vars

def test_filter_empty_returns_sorted():

    fake_env = {"Z_VAR": "2", "A_VAR": "1"}
    res = filter_env_vars(fake_env, [])  
    keys = list(res.keys())
    assert keys == ["A_VAR", "Z_VAR"], "Klucze nie są posortowane alfabetycznie"

def test_filter_case_insensitive():
    #ignorowanie wielkosci liter
    fake_env = {"Path": "C:/", "USER": "admin", "ignore": "this"}
    res = filter_env_vars(fake_env, ["path", "UsER"])
    
    assert "Path" in res
    assert "USER" in res
    assert "ignore" not in res

def test_filter_partial_match():
    #czesniowe dopasowanie
    fake_env = {"JAVA_HOME": "/opt/java", "HOME": "/home/user"}
    res = filter_env_vars(fake_env, ["home"])
    
    assert "JAVA_HOME" in res
    assert "HOME" in res