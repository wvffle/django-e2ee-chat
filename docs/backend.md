# Bledy
Wszystkie bledy zwracane przez API powinny byc w ponizszym formacie

Nastepujace kody bledow powinny miec globalne handlery: **500**, **404**, **405**, **418**
### Odpowiedz
```json5
{
  "message": "...",
  "success": false
}
```

# Endpointy

## `POST /register`
### Zapytanie
```json5
{
  "publicKey": "....",
  "hcaptcha": "...."
}
```

### Odpowiedz
```json5
{
  "id": "...",
  "success": true
}
```

### Bledy
- **401** - Taki klucz publiczny juz istnieje


## `POST /login`
### Zapytanie
```json5
{
  "publicKey": "....",
  // lub
  "id": "...."
}
```

### Odpowiedz
```json5
{
  "sessionKey": "....",
  "success": true
}
```

### Bledy
- **401** - Brak takiego klucza
- **403** - Klucz zostal zablokowany/zbanowany

## `POST /login/verify`
### Zapytanie
```json5
{
  "key": "...."
}
```

### Odpowiedz
```json5
{
  "success": true,
}
```

### Bledy
- **403** - Zle rozszyfrowany klucz

## `POST /chat/new`
### Zapytanie
```json5
{}
```

### Odpowiedz
```json5
{
  "success": true,
  "roomId": "..."
}
```

## `POST /chat/join`
### Zapytanie
```json5
{
  "roomId": "..."
}
```

### Odpowiedz
```json5
{
  "success": true
}
```

## `POST /chat/:id/accept`
### Zapytanie
```json5
{
  "accepted": true // or false
}
```

### Odpowiedz
```json5
{
  "success": true
}
```

### Bledy
- **401** - User nie jest adminem pokoju
- **403** - User nie jest w pokoju

## `POST /chat/:id/messages`
### Zapytanie
```json5
{
  "message": "...",
  "key": {
    id_1: "...",
    id_2: "..."
  }
}
```

### Odpowiedz
```json5
{
  "success": true
}
```

### Bledy
- **403** - User nie jest w pokoju
