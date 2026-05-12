

class Station:
    def __init__(self, kod_stacji, nazwa_stacji, data_uruchomienia, data_zamkniecia, typ_stacji, rodzaj_stacji, wojewodztwo, miejscowosc, adres, dl_geograficzna, szer_geograficzna):
        self.kod_stacji = kod_stacji
        self.nazwa_stacji = nazwa_stacji
        self.data_uruchomienia = data_uruchomienia
        self.data_zamkniecia = data_zamkniecia
        self.typ_stacji = typ_stacji
        self.rodzaj_stacji = rodzaj_stacji
        self.wojewodztwo = wojewodztwo
        self.miejscowosc = miejscowosc
        self.adres = adres
        self.dl_geograficzna = dl_geograficzna
        self.szer_geograficzna = szer_geograficzna

    def __str__(self):
        return f"Stacja {self.nazwa_stacji} o numerze {self.kod_stacji}, uruchomiona {self.data_uruchomienia} a zamknięta o {self.data_zamkniecia}, typ: {self.typ_stacji}, rodzaj: {self.rodzaj_stacji}, województwo {self.wojewodztwo}, miejscowość: {self.miejscowosc}, adres {self.adres}, koordynatty: {self.dl_geograficzna}, {self.szer_geograficzna}"
    def __repr__(self):
        return f"Station(kod_stacji={self.kod_stacji}, nazwa_stacji={self.nazwa_stacji}, data_uruchomienia={self.data_uruchomienia}, data_zamkniecia={self.data_zamkniecia}, typ_stacji={self.typ_stacji}, rodzaj_stacji={self.rodzaj_stacji}, wojewodztwo={self.wojewodztwo}, miejscowosc={self.miejscowosc}, adres={self.adres}, dl_geograficzna={self.dl_geograficzna}, szer_geograficzna={self.szer_geograficzna})"
    def __eq__(self, other):
        if isinstance(other, Station):
            return self.kod_stacji == other.kod_stacji
        return False
    
if __name__ == '__main__':
    stacja1 = Station("1","stacja pierwsza","2026-04-20","2026-05-20","typA","rodzajA","Dolnoślaskie","Wrocław","Rymarska 20G", "19.1234", "50.5678")
    stacja2 = Station("1","stacja druga","2026-04-20","2026-05-20","typA","rodzajA","Dolnoślaskie","Wrocław","Rymarska 20G", "19.1234", "50.5678")
    stacja3 = Station("3","stacja pierwsza","2026-04-20","2026-05-20","typA","rodzajA","Dolnoślaskie","Wrocław","Rymarska 20G", "19.1234", "50.5678")

    print(f"stacja1 == stacja2: {stacja1 == stacja2}")
    print(f"stacja1 == stacja3: {stacja1 == stacja3}")
    print(f"str: {stacja1}")
    print(f"repr: {repr(stacja1)}")