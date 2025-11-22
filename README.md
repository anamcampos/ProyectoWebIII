# Proyecto: Web Scraper (books.toscrape.com) con Selenium + Docker

## Resumen
Scraper que extrae items de books.toscrape.com, guarda en Postgres, expone una API (Flask) y un frontend simple.

## Requisitos
- Docker & docker-compose
- .env (copiar de .env.example y rellenar)

## Levantar
1. Copia `.env.example` a `.env` y ajusta variables.
2. Levanta servicios:
docker-compose up --build
3. API disponible en: `http://localhost:5000/`
4. Ejecuta una corrida manual:
docker exec -it books_web python main.py

## Notas
- Respeta robots.txt y términos de uso; books.toscrape.com es una web de pruebas.
- En producción, quita `max_pages` y ajusta delays para respetar el servidor.
- Para sitios que requieran autenticación, llena las variables LOGIN_* en `.env`.
