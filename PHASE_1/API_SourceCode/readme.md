# Description

API backend.

# Components

- database: For interacting with the database (local in production, cloud in development)
- dateparse: For parsing event dates from article main text.
- disease: For parsing diseases and syndromes from article main text.
- googlemaps: For parsing location from article main text.
- keyterms: For parsing key terms from article main text.
- scraper: For web scraping from WHO disease outbreak news (uses database, dateparse, disease, googlemaps and keyterms).
- server: For Flask web server (uses database).
