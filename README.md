Mały serwer (Python Flask) wyświetlający najbliższe odjazdy z trzech wybranych przystanków<br>

Funkcje wyszukujące odjazdy i rozkład jazdy znajdują sie w kontrolerach (app/views.py)<br>

Nazwy parametrów funkcji:<br>

busNum => numer autobusu <br>
stopID => ID przystanku autobusowego <br> 
o => nieznany parametr, najczęściej "02" lub "04"<br>
k => nieznany parametr, najczęściej "B" (stąd "B" jest w funkcjach ustawiony jako default) <br>

Aby strona poprawnie działała należy także dodać obrazek "busik.jpg" do folderu static oraz favico (swoich nie mogę udostępniać publicznie) - zobacz index.html
