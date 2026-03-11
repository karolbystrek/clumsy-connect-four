# Raport – Projekt EasyAI: Clumsy Connect Four

## Autorzy

| | Autor 1 | Autor 2 |
|---|---|---|
| **Imię i nazwisko** | Karol Bystrek| Patryk Chamera |
| **E-mail** | karbystrek@student.agh.edu.pl | pchamera@student.agh.edu.pl |
| **Numer indeksu** | TODO | 420201 |

---

## 1. Opis gry

### 1.1. Connect Four – wariant klasyczny (deterministyczny)

**Connect Four** (Połącz Cztery) to dwuosobowa gra strategiczna rozgrywana na planszy o wymiarach 6 wierszy × 7 kolumn. Gracze na zmianę wrzucają żetony (oznaczone symbolami `O` i `X`) do wybranej kolumny – żeton spada na najniższe wolne pole w danej kolumnie. Wygrywa ten gracz, który jako pierwszy ułoży cztery własne żetony w linii prostej: poziomej, pionowej lub ukośnej. Jeśli plansza zostanie całkowicie zapełniona bez osiągnięcia czterech w rzędzie przez żadnego z graczy, gra kończy się remisem.

### 1.2. Clumsy Connect Four – wariant probabilistyczny

**Clumsy Connect Four** to probabilistyczna modyfikacja klasycznej gry Connect Four. W tym wariancie żeton wrzucany przez gracza może „ześlizgnąć się" (*slip*) do sąsiedniej kolumny zamiast trafić do zamierzonej. Mechanizm ten wprowadza element losowości, który zmienia charakter gry z w pełni deterministycznego na stochastyczny.

**Zasady mechanizmu slip:**

- **Prawdopodobieństwo slip:** W przeprowadzonych eksperymentach najczęściej stosowaliśmy wartość **10%** (`slip_probability = 0.1`). Oznacza to, że z prawdopodobieństwem 10% żeton trafia do innej kolumny niż zamierzona.
- **Kierunek slip:** Jeśli dojdzie do ześlizgnięcia, żeton z równym prawdopodobieństwem (**50/50**) trafia do kolumny po lewej lub po prawej stronie zamierzonej kolumny.
- **Krawędzie planszy:**
  - Jeśli gracz celuje w **skrajną lewą kolumnę** (kolumna 0), slip może nastąpić wyłącznie w prawo (do kolumny 1).
  - Jeśli gracz celuje w **skrajną prawą kolumnę** (kolumna 6), slip może nastąpić wyłącznie w lewo (do kolumny 5).
- **Pełne kolumny:** Jeśli sąsiednia kolumna, do której miałby nastąpić slip, jest już pełna, żeton trafia do drugiej sąsiedniej kolumny. Jeśli **obie** sąsiednie kolumny są pełne, slip nie następuje i żeton trafia do oryginalnie zamierzonej kolumny (tak jakby slip nie wystąpił).

### 1.3. Implementacja

Gra została zaimplementowana w języku Python z wykorzystaniem biblioteki **easyAI**. Klasa `ConnectFour` dziedziczy po `TwoPlayerGame` z easyAI i rozszerza ją o mechanizm slip. Plansza jest reprezentowana jako tablica NumPy 6×7. Kluczowe elementy implementacji:

- **`clumsy_connect_four.py`** – implementacja logiki gry, w tym mechanizmu slip w metodzie `slip()` oraz nadpisanej metody `make_move()`.
- **`game_simulation.py`** – klasa `GameSimulation` odpowiedzialna za przeprowadzanie serii meczów między dwoma graczami AI, mierzenie czasów i zapis wyników do plików JSON.
- **Skrypty porównawcze** (`compare_*.py`) – konfiguracje poszczególnych eksperymentów.

---

## 2. Eksperymenty z AI – Negamax vs Negamax

W tej sekcji opisujemy eksperymenty, w których dwóch graczy AI z algorytmem **Negamax** grało przeciwko sobie wielokrotnie, z naprzemiennym graczem rozpoczynającym. Porównano dwa różne ustawienia maksymalnej głębokości na wariancie deterministycznym i probabilistycznym gry.

### 2.1. Eksperyment 1: Negamax (głębokość 9) vs Negamax (głębokość 9)

>  `output/compare_det_vs_nondet_d9/20260306_195818.json`

**Konfiguracja:**
- Gracz 1: Negamax (depth=9, pruning=True)
- Gracz 2: Negamax (depth=9, pruning=True)
- Liczba meczów: 20 (naprzemienne rozpoczynanie)

**Wyniki – wariant deterministyczny** (slip = 0.0):

| | Gracz 1 | Gracz 2 |
|---|:---:|:---:|
| **Zwycięstwa** | 10 | 10 |
| **Remisy** | 0 | 0 |
| **Śr. czas ruchu** | 2.995 s | 3.049 s |

**Wyniki – wariant probabilistyczny** (slip = 0.1):

| | Gracz 1 | Gracz 2 |
|---|:---:|:---:|
| **Zwycięstwa** | 9 | 10 |
| **Remisy** | 1 | – |
| **Śr. czas ruchu** | 4.498 s | 4.215 s |

**Obserwacje:** W wariancie deterministycznym wynik jest idealnie symetryczny (10:10) – gracz rozpoczynający wygrywa każdy mecz, co potwierdza, że przy identycznej głębokości przeszukiwania gra jest w pełni zdeterminowana. W wariancie probabilistycznym pojawia się element losowości – wynik 9:10 z 1 remisem pokazuje, że slip wprowadza nieprzewidywalność, powodując okazjonalne remisy i nieco inną dystrybucję wygranych. Czasy ruchów są wyraźnie dłuższe w wariancie probabilistycznym (~4.3 s vs ~3.0 s).

### 2.2. Eksperyment 2: Negamax (głębokość 7) vs Negamax (głębokość 9)

>  `output/negamax_depth_7_vs_9/20260306_195838.json`

**Konfiguracja:**
- Gracz 1: Negamax (depth=7, pruning=True)
- Gracz 2: Negamax (depth=9, pruning=True)
- Liczba meczów: 20

**Wyniki – wariant deterministyczny** (slip = 0.0):

| | Gracz 1 (d=7) | Gracz 2 (d=9) |
|---|:---:|:---:|
| **Zwycięstwa** | 10 | 10 |
| **Remisy** | 0 | 0 |
| **Śr. czas ruchu** | 0.375 s | 3.107 s |

**Wyniki – wariant probabilistyczny** (slip = 0.1):

| | Gracz 1 (d=7) | Gracz 2 (d=9) |
|---|:---:|:---:|
| **Zwycięstwa** | 6 | 12 |
| **Remisy** | 2 | – |
| **Śr. czas ruchu** | 0.629 s | 5.072 s |

**Obserwacje:** W wariancie deterministycznym oba algorytmy osiągają identyczny wynik (10:10), co oznacza, że przy naprzemiennym rozpoczynaniu gracz otwierający partię wygrywa niezależnie od głębokości przeszukiwania. W wariancie probabilistycznym większa głębokość (d=9) daje wyraźną przewagę – gracz z głębokością 9 wygrywa 12 meczów wobec 6 gracza z głębokością 7. Sugeruje to, że **w wariancie probabilistycznym dalsza analiza drzewa gry pozwala lepiej radzić sobie z niepewnością** spowodowaną mechanizmem slip. Koszt czasowy jest jednak znacząco wyższy (~5.1 s vs ~0.6 s na ruch).

### 2.3. Napotkane problemy

#TODO

---

## 3. Porównanie algorytmów – Negamax z i bez odcięcia alfa-beta

W tej sekcji porównujemy algorytm Negamax z odcięciem alfa-beta (`pruning=True`) oraz bez odcięcia (`pruning=False`) dla dwóch ustawień głębokości (5 i 7) na wariantach deterministycznym i probabilistycznym. Dodatkowo porównujemy algorytm Negamax z algorytmem SSS*.

### 3.1. Negamax z alfa-beta vs bez alfa-beta – głębokość 5

>  `output/negamax_ab_vs_no_ab_d5/20260306_220005.json` (run 1) oraz `output/negamax_ab_vs_no_ab_d5/20260309_192259.json` (run 2)

**Konfiguracja:**
- Gracz 1: Negamax (depth=5, pruning=**True**)
- Gracz 2: Negamax (depth=5, pruning=**False**)
- Liczba meczów: 20

#### Run 1 (`20260306_220005.json`)

**Wyniki – wariant deterministyczny** (slip = 0.0):

| | Gracz 1 (z α-β) | Gracz 2 (bez α-β) |
|---|:---:|:---:|
| **Zwycięstwa** | 10 | 10 |
| **Remisy** | 0 | 0 |
| **Śr. czas ruchu** | 0.043 s | 0.932 s |

**Wyniki – wariant probabilistyczny** (slip = 0.1):

| | Gracz 1 (z α-β) | Gracz 2 (bez α-β) |
|---|:---:|:---:|
| **Zwycięstwa** | 8 | 8 |
| **Remisy** | 4 | – |
| **Śr. czas ruchu** | 0.062 s | 1.511 s |

#### Run 2 (`20260309_192259.json`)

**Wyniki – wariant deterministyczny** (slip = 0.0):

| | Gracz 1 (z α-β) | Gracz 2 (bez α-β) |
|---|:---:|:---:|
| **Zwycięstwa** | 10 | 10 |
| **Remisy** | 0 | 0 |
| **Śr. czas ruchu** | 0.065 s | 1.345 s |

**Wyniki – wariant probabilistyczny** (slip = 0.1):

| | Gracz 1 (z α-β) | Gracz 2 (bez α-β) |
|---|:---:|:---:|
| **Zwycięstwa** | 10 | 7 |
| **Remisy** | 3 | – |
| **Śr. czas ruchu** | 0.091 s | 2.203 s |

**Obserwacje:** Odcięcie alfa-beta nie wpływa na jakość decyzji w wariancie deterministycznym (wynik 10:10 w obu runach), ale **drastycznie skraca czas obliczeń** – z odcięciem alfa-beta ruch zajmuje ok. 0.04–0.09 s wobec 0.93–2.20 s bez odcięcia (przyspieszenie ok. **15–25×**). W wariancie probabilistycznym wyniki rozchodzą się między runami (8:8 w run 1, 10:7 w run 2), co odzwierciedla losową naturę gry.

### 3.2. Negamax z alfa-beta vs bez alfa-beta – głębokość 7

>  `output/negamax_ab_vs_no_ab_d7/20260306_195823.json`

**Konfiguracja:**
- Gracz 1: Negamax (depth=7, pruning=**True**)
- Gracz 2: Negamax (depth=7, pruning=**False**)
- Liczba meczów: 5 (mniejsza liczba ze względu na ogromny czas obliczeń bez pruning)

**Wyniki – wariant deterministyczny** (slip = 0.0):

| | Gracz 1 (z α-β) | Gracz 2 (bez α-β) |
|---|:---:|:---:|
| **Zwycięstwa** | 2 | 3 |
| **Remisy** | 0 | 0 |
| **Śr. czas ruchu** | 0.355 s | 47.292 s |

**Wyniki – wariant probabilistyczny** (slip = 0.1):

| | Gracz 1 (z α-β) | Gracz 2 (bez α-β) |
|---|:---:|:---:|
| **Zwycięstwa** | 1 | 4 |
| **Remisy** | 0 | 0 |
| **Śr. czas ruchu** | 0.422 s | 56.962 s |

**Obserwacje:** Przy głębokości 7 różnica w wydajności jest jeszcze bardziej dramatyczna. Negamax bez odcięcia alfa-beta potrzebuje średnio **~47–57 sekund** na pojedynczy ruch, podczas gdy z odcięciem alfa-beta jest to jedynie **~0.35–0.42 sekundy** – przyspieszenie rzędu **130×**. Mimo to jakość decyzji pozostaje identyczna – brak odcięcia alfa-beta nie poprawia wyników gry, jedynie dramatycznie wydłuża czas obliczeń. Ze względu na ekstremalny czas trwania eksperymentu, liczbę meczów ograniczono do 5.

### 3.3. Negamax (z α-β) vs SSS* – głębokość 7

>  `output/negamax_vs_sss_d7/20260306_195848.json`

**Konfiguracja:**
- Gracz 1: Negamax (depth=7, pruning=True)
- Gracz 2: SSS* (depth=7)
- Liczba meczów: 20

**Wyniki – wariant deterministyczny** (slip = 0.0):

| | Gracz 1 (Negamax) | Gracz 2 (SSS*) |
|---|:---:|:---:|
| **Zwycięstwa** | 10 | 10 |
| **Remisy** | 0 | 0 |
| **Śr. czas ruchu** | 0.417 s | 0.743 s |

**Wyniki – wariant probabilistyczny** (slip = 0.1):

| | Gracz 1 (Negamax) | Gracz 2 (SSS*) |
|---|:---:|:---:|
| **Zwycięstwa** | 11 | 7 |
| **Remisy** | 2 | – |
| **Śr. czas ruchu** | 0.549 s | 0.960 s |

**Obserwacje:** W wariancie deterministycznym oba algorytmy osiągają identyczny wynik (10:10). W wariancie probabilistycznym **Negamax z odcięciem alfa-beta radzi sobie nieco lepiej niż SSS*** (11:7). SSS* jest nieco wolniejszy od Negamaxa z alfa-beta (~0.74–0.96 s vs ~0.42–0.55 s), ale różnica ta jest znacznie mniejsza niż w porównaniu z Negamaxem bez odcięcia.

### **Kluczowe wnioski dotyczące wydajności:**

1. **Odcięcie alfa-beta** przynosi ogromne przyspieszenie: ~20× przy głębokości 5 i ~130× przy głębokości 7. Efekt rośnie wykładniczo z głębokością.
2. **Wariant probabilistyczny** jest konsekwentnie wolniejszy od deterministycznego (o ~30–50%), ponieważ gry trwają średnio dłużej ze względu na remisy i mniej przewidywalne pozycje.
3. **SSS*** jest szybciej niż Negamax bez odcięcia, ale wolniejszy niż Negamax z alfa-beta, co sugeruje że w tym kontekście klasyczne odcięcie alfa-beta jest najbardziej efektywną optymalizacją.
4. **Zwiększenie głębokości** z 7 do 9 zwiększa czas ruchu ok. 5–8× (z ~0.4 s do ~3.0 s z alfa-beta).

---


