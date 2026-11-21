# System rozproszony REST API – Serwis Produktów i Serwis Magazynowy

Dwa niezależne mikroserwisy w Pythonie (FastAPI), komunikujące się przez REST.

| Serwis            | Port | Endpoint                 | Odpowiedź (200)                                  |
|-------------------|------|--------------------------|--------------------------------------------------|
| Serwis Produktów  | 8001 | `GET /products/{id}`     | `{ "id": 123, "name": "Laptop", "price": 4500.0 }` |
| Serwis Magazynowy | 8002 | `GET /stock/{productId}` | `{ "productId": 123, "quantity": 15 }`           |

Serwis Magazynowy przy każdym zapytaniu odpytuje Serwis Produktów
(`GET /products/{id}`), żeby sprawdzić, czy produkt istnieje:

```
Klient --GET /stock/123--> Serwis Magazynowy --GET /products/123--> Serwis Produktów
```

Kody błędów:

- `404` – produkt nie istnieje (oba serwisy)
- `503` – Serwis Magazynowy nie może połączyć się z Serwisem Produktów

Dostępne produkty (dane w pamięci): `123`, `124`, `125`.

## Wymagania

- Python 3.10+

## Instalacja

```bash
git clone <https://github.com/LosCasperos/rest-microservices.git>
cd <https://github.com/LosCasperos/rest-microservices.git>

python -m venv .venv
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

python -m pip install -r requirements.txt
```

## Uruchomienie

Każdy serwis w osobnym terminalu (w obu aktywuj najpierw `.venv`).

Terminal 1 – Serwis Produktów (`localhost:8001`):

```bash
python product_service/main.py
```

Terminal 2 – Serwis Magazynowy (`localhost:8002`):

```bash
python stock_service/main.py
```

## Testowanie

```bash
# Scenariusz sukcesu – produkt istnieje
curl -i http://localhost:8002/stock/123

# Scenariusz błędu – produkt nie istnieje (404)
curl -i http://localhost:8002/stock/999

# Serwis Produktów bezpośrednio
curl -i http://localhost:8001/products/123
```

W PowerShellu użyj `curl.exe` zamiast `curl`.

Interaktywna dokumentacja (Swagger UI): <http://localhost:8001/docs> i <http://localhost:8002/docs>.
