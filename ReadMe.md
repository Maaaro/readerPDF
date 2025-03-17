Program jest używany do wykazania wkładu własnego przed Bankiem.
Wkład własny wykazuje się prezentując fakturę i wyciąg bankowy - potwierdzenie zakupu i potwierdzenie zapłaty.

Tego programu można użyć, żeby znaleźć dokumenty odpowiadające numerom faktur.

Na wejściu:
- Lista spraw (aktualnie jako excel)
    - sprawa zawiera numer faktury dostawcy
    - sprawa zawiera opcjonalnie numer workflowowy
    - sprawa zawiera porządaną prefix nazwy pliku

- Ściezkę katalogu z fakturami dostawcy <source>
  - Pliki faktur (w formacie pdf)
  - Plik faktury ma w sobie numer faktury dostawcy
  - Plik może być albo luźno, albo być zagnieżdżony w katalogu który ma nazwę sprawy workflow

- Ograniczenie wyszukiwania: tak/nie
- Suffix wynikowej nazwy pliku albo "_fv" albo "_wb"

- Ścieżka do katalogu wynikowego <target>

Na wyjściu:

- Informacja o niepoprawnych danych wejściowych:
  - wejściowy plik z listą spraw jest niepoprawny
  - lista spraw nie ma koniecznej kolumny
  - folder <source> jest pusty
- Modyfikacja pliku wejściowego (excel), z dodaniem do niego kolumny i uzupełnieni informacji o powodzeniu przetwarzani
  (niepoprawna faktura dostawcy, faktura jest zdjęciem, nie znaleziono faktury o podanym numerze)
- Znalezione pliki faktur są umieszczone w <target> z nadaną nazwą `<prefix>-<id>-<suffix>.pdf`, gdzie prefix
  to porządany prefiks nazwy pliku sprawy a `id` to liczba porządkowa, jeśli znaleziono więcej niż jeden.
  Gdzie suffix to jest albo "_fv" albo "_wb"

User story #1

- Marek sam szuka dokumentów, wybiera tryb "wyciagi bankowe", i wtedy folder <source> z fakturami zawiera
  luźne pliki pdf, z których trzeba szukać.

User story #2:

- Marek podaje informatykowi listę spraw workflow, i oddaje Markowi wszystkie dokumenty przypisane do tej sprawy.
  Dostaje `dokumenty dla Marka/` <source>, tam jest nazwa która katalogu jest 1:1 z numerem workflow,
  i wtedy Marek zaznacza tryb "faktury", i wtedy program, jeśli sprawa ma uzupełniony numer workflow,
  to program otwiera katalog o tym numerze, i stamtąd filtruje faktury znowu po numerze faktury dostawy.
  i tam też mogą być pliki które nie są pdf, więc program powinien nie patrzeć na nie .pdf.

Potencjalna implementacja:
- jeśli tryb pracy to "faktury", to program ogranicza wyszukiwania spraw
- te faktury z listy spraw, mają być przekopiowane z source do target
  Jeśli znaleziono fakturę `source/Dokument_F_000895_23_RO.pdf` z numerem bankowym `54`, to ma stworzyć plik `target/54.pdf`
  Jeśli znaleziono kilka, to wtedy `target/54-1.pdf`
- informacja per-sprawa, czy udało się wczytać/przenieść plik faktury dostawcy
- jeśli liczba porzadkowa ma duplikaty albo jej nie ma, to powiedz że plik wejściowy excel jest niepoprawny.
- jeśli plik faktury dostawcy jest niepoprawny/uszkodzony to ma dodać komentarz do sprawy o statusie dokumentu
