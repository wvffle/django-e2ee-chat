# Rejestracja
User wysyla request `POST /register` z kluczem publicznym oraz captcha, serwer generuje losowy identyfikator (base58, 8 znakow) i zapisuje w bazie danych, ze ten identyfikator to ten klucz publiczny. Nastepnie zwraca odpowiedz.

# Logowanie
Uzytkownik wrzuca swoje klucze prywatne i publiczne do frontednu.

Frontend wysyla zapytanie `POST /login` z identyfikatorem. Jezeli klucza nie ma w bazie - rzucamy 401, jezeli klucz jest zbanowany rzucamy 403. Jezeli wszystko jest okej - generujemy na serwerze klucz sesji (AES), zapisujemy go w modelu usera, po czym szyfrujemy kluczem publicznym uzytkownika wraz z losowym stringiem (32 znaki, base58) i nastepnie wysylamy zaszyfrowane stringi w odpowiedzi. Zapisujemy losowy string (klucz autentykacyjny) w cache na 15 min.
Frontend przechwytuje string i stara sie go rozszyfrowac uzywajac klucza prywatnego.

**⚠ ⚠ ⚠ OD TEGO MOMENTU WSZYSTKIE ZAPYTANIA/ODPOWIEDZI SA SZYFROWANE KLUCZEM SESYJNYM (AES) ⚠ ⚠ ⚠️**

Nastepnie wysylane jest zapytanie `POST /login/verify` z rozszyfrowanym (lub nie) strigniem, serwer sprawdza czy przeslany klucz autentykacyjny jest w cache. Jezeli tak, zwracamy pozytywna odpowiedz, jezeli nie - rzucamy bledem 403.


# Nowy pokoj
Uzytkownik wysyla puste zapytanie `POST /chat/new`. W odpowiedzi dostaje id nowego pokoju (base58, 8 znakow).

# Dolaczenie do pokoju
Uzyszkodnik wysyla zapytanie `POST /chat/join`, podaje identyfikator pokoju do ktorego chce dolaczyc. Administrator pokoju wybiera czy zezwolic czy nie.

# Akceptacja nowych uzytkownikow w pokojach
Administrator pokoju wysyla zapytanie `POST /chat/:id/accept` (`:id` to identyfikator pokoju) i podaje, czy zaakceptowal czy nie

# Pollowanie powiadomien o zmianie stanu
User wysyla zapytanie `GET /state` co 5s, w odpowiedzi dostaje nowy stan.

# Wysylanie wiadomosci w pokoju
Uzytkownik wysyla zapytanie `POST /chat/:id/messages` (gdzie `:id` to identyfikator pokoju). I tu zaczyna sie jazda.

NA FRONTENDZIE:
Generowany jest klucz AES.
Wiadomosc jest szyfrowana kluczem AES, nastepnie klucz aes jest szyfrowany przez wszystkie klucze publiczne w pokoju.

Wysylana jest nastepujaca tresc:
```json5
{
  message: "....", // Wiadomosc zaszyfrowana kluczem AES
  key: {
    id_usera_1: "....", // Zaszyfrowany klucz AES kluczem publicznym usera pierwszego
    id_usera_2: "...." // Zaszyfrowany klucz AES kluczem publicznym usera drugiego
    // ... (i tak dla wszystkich osob w danym pokoju)
  }
}
```

Serwer dodaje ta wiadomosc do stanu pokoju
