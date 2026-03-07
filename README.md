# Clumsy Connect Four - Analiza Algorytmów Sztucznej Inteligencji

Projekt koncentruje się na analizie i porównaniu wydajności różnych algorytmów sztucznej inteligencji w grze Connect Four (Czwórki) z wprowadzeniem mechaniki losowości ("slip"). Badania obejmują algorytmy Negamax (z i bez odcinania alfa-beta) oraz SSS, testowane na różnych głębokościach przeszukiwania w środowiskach deterministycznych i niedeterministycznych.

## Przegląd gry Clumsy Connect Four

Clumsy Connect Four to wariant klasycznej gry "Czwórki", rozgrywanej na planszy o wymiarach 6x7. Standardowe zasady wymagają od graczy naprzemiennego wrzucania żetonów do kolumn, dążąc do ułożenia czterech elementów swojego koloru w linii pionowej, poziomej lub ukośnej.

### Mechanika "Slip" (Poślizg)

Kluczową innowacją w tym projekcie jest wprowadzenie parametru `slip_probability`. Określa on prawdopodobieństwo, z jakim żeton "ześlizgnie się" do sąsiedniej kolumny (lewej lub prawej) podczas wykonywania ruchu. 

Właściwości mechaniki poślizgu:
- Jeśli poślizg nastąpi, żeton trafia do losowo wybranej sąsiedniej kolumny, o ile nie jest ona pełna.
- Mechanika ta przekształca grę z pełną informacją i deterministyczną w grę z elementem losowym.
- Wartość `slip_probability = 0.1` oznacza, że w 10% przypadków agent nie ma pełnej kontroli nad miejscem, w którym wyląduje jego żeton.

## Metodologia AI

W projekcie wykorzystano bibliotekę `easyAI` do zaimplementowania i przetestowania trzech podejść do podejmowania decyzji przez agentów.

### Wykorzystane algorytmy

- **Negamax**: Podstawowy algorytm przeszukiwania drzewa gry dla gier o sumie zerowej. W swojej czystej formie sprawdza on wszystkie możliwe stany do zadanej głębokości.
- **Odcinanie Alfa-Beta (Alpha-Beta Pruning)**: Rozszerzenie algorytmu Negamax, które pozwala na eliminację (odcinanie) gałęzi drzewa, które nie mają szans na poprawę wyniku gracza. Jest to kluczowa optymalizacja umożliwiająca przeszukiwanie głębszych warstw w krótszym czasie.
- **SSS (State Space Search)**: Algorytm przeszukiwania przestrzeni stanów, który w niektórych przypadkach może być bardziej wydajny niż standardowy Negamax z odcinaniem alfa-beta, poprzez bardziej selektywne badanie stanów.

### Głębokość przeszukiwania (Depth)

Głębokość przeszukiwania determinuje, ile ruchów w przód (zarówno własnych, jak i przeciwnika) agent bierze pod uwagę:
- **Depth 5**: Poziom podstawowy, pozwalający na bardzo szybką reakcję, ale podatny na błędy taktyczne.
- **Depth 7**: Poziom średniozaawansowany, stanowiący kompromis między czasem a jakością gry.
- **Depth 9**: Poziom zaawansowany, wymagający znacznych zasobów czasowych, zwłaszcza w wariancie bez optymalizacji alfa-beta.

### Funkcja oceny (Heuristic Scoring)

Ze względu na prostotę gry Connect Four, zastosowano binarną funkcję punktacji:
- **100**: Zwycięstwo gracza.
- **-100**: Zwycięstwo przeciwnika (przegrana).
- **0**: Brak rozstrzygnięcia na danej głębokości lub remis.

Tak prosta funkcja wymusza na agentach dążenie do zwycięstwa lub unikanie porażki, ale nie promuje "dobrych pozycji" w trakcie gry, co zwiększa znaczenie głębokości przeszukiwania.

## Eksperymenty i wyniki

W ramach projektu przeprowadzono serię symulacji, mających na celu zbadanie wpływu algorytmu, głębokości oraz losowości na wynik i czas gry.

### Eksperyment 1: Wpływ odcinania Alfa-Beta

Porównano wydajność czasową i skuteczność algorytmu Negamax z włączoną i wyłączoną optymalizacją Alfa-Beta.

**Głębokość 5 (20 meczów):**
| Wariant | Gracz 1 (A-B) | Gracz 2 (Bez A-B) | Remisy | Czas ruchu G1 [s] | Czas ruchu G2 [s] |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Deterministyczny | 10 | 10 | 0 | 0.043 | 0.932 |
| Niedeterministyczny | 8 | 8 | 4 | 0.062 | 1.511 |

**Głębokość 7 (5 meczów):**
| Wariant | Gracz 1 (A-B) | Gracz 2 (Bez A-B) | Remisy | Czas ruchu G1 [s] | Czas ruchu G2 [s] |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Deterministyczny | 2 | 3 | 0 | 0.355 | 47.292 |
| Niedeterministyczny | 1 | 4 | 0 | 0.422 | 56.962 |

*Uwaga: Ze względu na bardzo długi czas obliczeń bez optymalizacji Alfa-Beta (ponad 100 razy wolniej przy Depth 7), liczba meczów w tym wariancie została ograniczona do 5.*

### Eksperyment 2: Wpływ głębokości przeszukiwania (Depth 7 vs 9)

Badanie przewagi agenta analizującego głębsze stany drzewa gry (20 meczów).

| Wariant | Depth 7 Wygrane | Depth 9 Wygrane | Remisy | Czas ruchu D7 [s] | Czas ruchu D9 [s] |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Deterministyczny | 10 | 10 | 0 | 0.375 | 3.107 |
| Niedeterministyczny | 6 | 12 | 2 | 0.629 | 5.072 |

W środowisku niedeterministycznym głębokość 9 zapewnia wyraźną przewagę nad głębokością 7, co sugeruje, że lepsze planowanie pozwala częściowo niwelować skutki losowych poślizgów.

### Eksperyment 3: Negamax vs SSS (Głębokość 7)

Porównanie dwóch różnych algorytmów przeszukiwania na tej samej głębokości (20 meczów).

| Wariant | Negamax Wygrane | SSS Wygrane | Remisy | Czas ruchu Negamax [s] | Czas ruchu SSS [s] |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Deterministyczny | 10 | 10 | 0 | 0.417 | 0.743 |
| Niedeterministyczny | 11 | 7 | 2 | 0.549 | 0.960 |

Algorytmy wykazują zbliżoną skuteczność, jednak Negamax z odcinaniem Alfa-Beta okazał się nieznacznie szybszy i bardziej odporny na niedeterminizm środowiska.

### Eksperyment 4: Środowisko deterministyczne vs niedeterministyczne

Analiza wpływu mechaniki poślizgu na czas obliczeń przy stałej głębokości (Depth 9, 20 meczów).

| Wariant | Średni czas ruchu [s] | Maksymalny czas meczu | Remisy |
| :--- | :---: | :---: | :---: |
| Deterministyczny | 3.02 | Krótki (brak pomyłek) | 0 |
| Niedeterministyczny | 4.36 | Długi (więcej ruchów) | 1 |

Wprowadzenie losowości wydłuża czas namysłu agentów oraz średnią długość rozgrywki, gdyż "błędy" wynikające z poślizgów wymagają od agentów korygowania planów i szukania nowych dróg do zwycięstwa.

## Wnioski i wyzwania

Analiza wyników eksperymentalnych pozwala na sformułowanie następujących wniosków:

1.  **Krytyczne znaczenie optymalizacji Alfa-Beta**: Bez odcinania zbędnych gałęzi drzewa, algorytm Negamax staje się niepraktyczny już na głębokości 7. Czas potrzebny na podjęcie decyzji rośnie wykładniczo, co uniemożliwia płynną rozgrywkę i masowe testowanie algorytmów w tym wariancie.
2.  **Adaptacja do niedeterminizmu**: Mechanika "slip" sprawia, że gra w Czwórki przestaje być grą o pełnej informacji z przewidywalnym wynikiem. Nawet optymalny ruch może przynieść negatywne skutki, co faworyzuje agentów o większej głębokości przeszukiwania (Depth 9), którzy potrafią lepiej ocenić alternatywne scenariusze po ewentualnym poślizgu.
3.  **Wydajność algorytmu SSS**: Algorytm SSS okazał się ciekawą alternatywą dla Negamax, oferując zbliżoną skuteczność przy nieco innym rozkładzie czasu obliczeń. Jednak w specyficznych warunkach gry Connect Four, klasyczny Negamax z optymalizacjami pozostaje najbardziej stabilnym rozwiązaniem.
4.  **Uproszczona heurystyka**: Zastosowanie punktacji zero-jedynkowej (wygrana/przegrana) sprawia, że agenci są bardzo skuteczni w końcowych fazach gry, ale mogą podejmować suboptymalne decyzje na początku partii. Rozbudowa funkcji o ocenę zajętych pól (np. przewaga w kolumnach środkowych) mogłaby zwiększyć siłę gry bez konieczności pogłębiania przeszukiwania.

### Podsumowanie techniczne

Projekt pokazał, że nawet niewielka zmiana w mechanice gry (10% szans na błąd ruchu) diametralnie zmienia wymagania stawiane algorytmom przeszukiwania przestrzeni stanów. Stabilność i wydajność czasowa stają się wówczas równie ważne, co sama jakość wybranego ruchu.

