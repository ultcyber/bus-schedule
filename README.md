Mały serwer (Python Flask) wyświetlający najbliższe odjazdy z trzech wybranych przystanków

Funkcje wyszukujące odjazdy i rozkład jazdy znajdują sie w kontrolerach (app/views.py)

Nazwy parametrów funkcji:

busNum => numer autobusu 
stopID => ID przystanku autobusowego 
o => nieznany parametr, najczęściej "02" lub "04"
k => nieznany parametr, najczęściej "B" (stąd "B" jest w funkcjach ustawiony jako default)

Aby strona poprawnie działała należy także dodać obrazek "busik.jpg" do folderu static oraz favico (swoich nie mogę udostępniać publicznie) - zobacz index.html
