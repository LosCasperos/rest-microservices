"""Serwis Produktów - zarządza informacjami o produktach.

Kontrakt:
    GET /products/{id} -> 200 {"id": 123, "name": "Laptop", "price": 4500.0}
                       -> 404 {"detail": "..."} gdy produkt nie istnieje
"""

import logging

import uvicorn
from fastapi import FastAPI, HTTPException

HOST = "127.0.0.1"
PORT = 8001

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [PRODUCT-SERVICE] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("product_service")

app = FastAPI(title="Serwis Produktów")

# Dane "na sztywno" w pamięci: id produktu -> dane produktu
PRODUCTS = {
    123: {"id": 123, "name": "Laptop", "price": 4500.00},
    124: {"id": 124, "name": "Monitor", "price": 1200.00},
    125: {"id": 125, "name": "Klawiatura", "price": 350.00},
}


@app.get("/products/{id}")
def get_product(id: int):
    log.info("Odebrano zapytanie o produkt id=%s", id)

    product = PRODUCTS.get(id)
    if product is None:
        log.info("Produkt id=%s nie istnieje -> 404", id)
        raise HTTPException(status_code=404, detail=f"Produkt o id {id} nie istnieje")

    log.info("Zwracam dane produktu: %s", product)
    return product


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
