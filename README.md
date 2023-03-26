# MTG Price Fetcher
> A simple price and sale fetcher for Magic: The Gathering, powered via Scryfall and TCGPlayer's API and written in Python.




Start the API with...
```
    pip install -r requirements-base.txt
    hypercorn preordain.main:app
```
Written documentation is a WIP. Location is currently [here](docs/api_functions.md). More functions will be added and documented over time.


Check out the dashboard @ localhost:8000/docs
![image](https://user-images.githubusercontent.com/73682114/223646534-da46b06e-622b-41b7-8ec9-ffc54898556e.png)

------------


- [MTG Price Fetcher](#mtg-price-fetcher)
  - [Features](#features)
  - [**To Do:**](#to-do)
  - [Libraries](#libraries)
    - [Base](#base)
    - [Dev](#dev)

## Features
*This list is non-exhaustive.*
- API
  - Organize and track personal inventory
    - Compare current price vs purchase price.
    - Add, delete, and clear current inventory.
  - Fetch fresh price data (provided from Scryfall)
    - See individual card prices
      - USD, Euro, and Tix, including Day over Day changes
    - Examine Top gains / losses over USD / Euro / Tix
  - View and catagorize various cards as different groups
- Scraper
  - Automatically scrape Scryfall price data and TCGPlayer sale data

## **To Do:**

  Just check [here](https://github.com/sbyt32/mtg_price_fetcher/discussions/22)


## Libraries
  ### Base
    arrow
    hypercorn
    psycopg[binary]
    fastapi<0.95.0
    python-dateutil
    requests
    httpx
    python-dotenv
  ### Dev
    flake8
    black
    pytest
    pytest-cov
    pre-commit
    pip-tools
