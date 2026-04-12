import os
import zad4


def uruchom_testy():
    dane_testowe = """Nr,Kod stacji,Nazwa stacji,WGS84 φ N,WGS84 λ E,Data uruchomienia,Data zamknięcia,Rodzaj stacji
    1,WrocMOB,Bogatynia - Chopina,50.123456,14.123456,2020-01-01,2021-12-31,mobilna
    2,ZlyMOB,Jelenia  Góra,200.000000,10.000000,,2022-13-45,stacjonarna
    3,Kod123,Bielsko - Biała - Centrum,51.123456,15.123456,1999-05-05,,tło
    4,War1,"Warszawa, ul. Marszałkowska",-90.000000,180.000000,2010-10-10,,przemysłowa
    5,Kra1,"Kraków, AL. Pokoju",45.000000,20.000000,,,tło
    6,Zwykla,Kędzierzyn-Koźle,40.123456,12.123456,2005-01-01,,tło
    """
    nazwa_pliku_testowego = "test_stacje.csv"
    with open(nazwa_pliku_testowego, "w", encoding="utf-8") as f:
        f.write(dane_testowe)

    print("start\n")

    try:

        daty = zad4.get_dates(nazwa_pliku_testowego)
        assert "2020-01-01" in daty, "Błąd: Brak poprawnej daty uruchomienia"
        assert "2021-12-31" in daty, "Błąd: Brak poprawnej daty zamknięcia"
        assert "2022-13-45" not in daty, "Błąd: Regex przepuścił nieistniejący miesiąc!"
        print("T 1 (daty) zaliczony!")

        lokalizacje = zad4.get_locations(nazwa_pliku_testowego)
        assert (50.123456, 14.123456) in lokalizacje, "Błąd: Brak poprawnej lokalizacji"
        assert (-90.0, 180.0) in lokalizacje, "Błąd: Brak poprawnej lokalizacji na granicy mapy"
        assert len(lokalizacje) == 5, f"Błąd: Znalazło złą liczbę lokalizacji: {len(lokalizacje)}"
        print("T 2 (wspolrzedne) zaliczony!")

        dziwne = zad4.get_werid_name_stations(nazwa_pliku_testowego)
        assert "Bogatynia - Chopina" in dziwne, "Błąd: Nie znalazło stacji z jednym myślnikiem"
        print("T 3 (-) zaliczony!")


        czyste = zad4.change_spaces(nazwa_pliku_testowego)
        assert "Bogatynia_-_Chopina" in czyste, "Błąd: Źle zamienione spacje wokół myślnika"
        assert "Jelenia_Gora" in czyste, "Błąd: Podwójna spacja nie zmieniła się w jedną podłogę!"
        assert "Krakow,_AL._Pokoju" in czyste, "Błąd: Polskie znaki (ó) nie zostały zamienione na o"
        print("T 4 (czyszczenie znaków) zaliczony!")

        mob = zad4.mob_ending_stations(nazwa_pliku_testowego)
        assert mob is False, "Błąd: Weryfikacja przepuściła stację MOB, która jest stacjonarna!"
        print(" T5 (weryfikacja MOB) passed!")

        trzy = zad4.separated_locations(nazwa_pliku_testowego)
        assert "Bielsko - Biała - Centrum" in trzy, "Błąd: Nie wyłapało 3 członów"
        print("T 6 (3 czlony) passed")


        ulice = zad4.stacje_z_ulica(nazwa_pliku_testowego)
        assert "Warszawa, ul. Marszałkowska" in ulice, "Błąd: Nie wyłapało małego ul."
        assert "Kraków, AL. Pokoju" in ulice, "Błąd: Flaga IGNORECASE nie zadziałała dla AL."
        print("T 7 (Ul ,) zaliczony!")



    finally:

        if os.path.exists(nazwa_pliku_testowego):
            os.remove(nazwa_pliku_testowego)

uruchom_testy()