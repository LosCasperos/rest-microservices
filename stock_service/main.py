"""Serwis Magazynowy - zarządza stanem magazynowym produktów.

Przed zwróceniem stanu pyta Serwis Produktów, czy produkt w ogóle istnieje.

Kontrakt:
    GET /stock/{productId} -> 200 {"productId": 123, "quantity": 15}
                           -> 404 gdy produkt nie istnieje w Serwisie Produktów
                           -> 503 gdy Serwis Produktów jest niedostępny
"""

import logging
import os

import httpx
import uvicorn
from fastapi import FastAPI, HTTPException, Path

HOST = "127.0.0.1"
PORT = 8002
# Adres Serwisu Produktów - można nadpisać zmienną środowiskową
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://127.0.0.1:8001")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [STOCK-SERVICE] %(message)s",
    datefmt="%H:%M:%S",
)
# httpx sam loguje każde wychodzące zapytanie - tu wystarczą nasze własne logi
logging.getLogger("httpx").setLevel(logging.WARNING)
log = logging.getLogger("stock_service")

app = FastAPI(title="Serwis Magazynowy")

# Dane "na sztywno" w pamięci: id produktu -> ilość w magazynie
STOCK = {
    123: 15,
    124: 40,
    125: 0,
}


def product_exists(product_id: int) -> bool:
    """Pyta Serwis Produktów, czy produkt o danym id istnieje."""
    url = f"{PRODUCT_SERVICE_URL}/products/{product_id}"
    log.info("Wysyłam zapytanie do Serwisu Produktów: GET %s", url)

    try:
        response = httpx.get(url, timeout=5.0)
    except httpx.RequestError as exc:
        log.error("Serwis Produktów jest niedostępny: %s", exc)
        raise HTTPException(status_code=503, detail="Serwis Produktów jest niedostępny")

    log.info("Odpowiedź Serwisu Produktów: %s %s", response.status_code, response.text)

    if response.status_code == 404:
        return False
    if response.status_code == 200:
        return True

    raise HTTPException(
        status_code=502,
        detail=f"Nieoczekiwana odpowiedź Serwisu Produktów: {response.status_code}",
    )


@app.get("/stock/{productId}")
def get_stock(product_id: int = Path(alias="productId")):
    log.info("Odebrano zapytanie o stan magazynowy productId=%s", product_id)

    if not product_exists(product_id):
        log.info("Produkt productId=%s nie istnieje -> 404", product_id)
        raise HTTPException(
            status_code=404, detail=f"Produkt o id {product_id} nie istnieje"
        )

    result = {"productId": product_id, "quantity": STOCK.get(product_id, 0)}
    log.info("Zwracam stan magazynowy: %s", result)
    return result


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
