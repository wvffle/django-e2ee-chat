# Bledy
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
- **500** - Mozliwe ze cos sie zepsuje na serwerze, wiec wtedy django powinno automatycznie rzucic HTTP 500


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
- **500** - Mozliwe ze cos sie zepsuje na serwerze, wiec wtedy django powinno automatycznie rzucic HTTP 500

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
- **500** - Mozliwe ze cos sie zepsuje na serwerze, wiec wtedy django powinno automatycznie rzucic HTTP 500
