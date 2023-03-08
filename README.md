# MTG Price Fetcher
> A simple price and sale fetcher for Magic: The Gathering, powered via Scryfall and TCGPlayer's API and written in Python.

This project contains a group of Python scripts that will allow the user to create a PostgreSQL database, and begin to scrape price data from Scryfall and TCGPlayer. It uses FastAPI to retrieve information from the database and returns in a .json format.


Start the API with...
```
    pip install -r requirements-base.txt
    python set_up.py
    hypercorn preordain.main:app
```
Written documentation is a WIP. Location is currently [here](docs/api_functions.md). More functions will be added and documented over time.


Check out the dashboard @ localhost:8000/docs
![image](https://user-images.githubusercontent.com/73682114/223646534-da46b06e-622b-41b7-8ec9-ffc54898556e.png)

------------


- [MTG Price Fetcher](#mtg-price-fetcher)
  - [Features](#features)
  - [How it works](#how-it-works)
    - [`set_up.py`](#set_uppy)
      - [`cfg_setup()`](#cfg_setup)
      - [`set_up_db()`](#set_up_db)
    - [`fetch_card_data.py`](#fetch_card_datapy)
    - [`logging_details.py`](#logging_detailspy)
    - [Testing (WIP)](#testing-wip)
  - [Libraries](#libraries)

## Features
*This list is non-exhaustive.*
- API
  - Search by Card Groups
  - Return price data of one or multiple cards
    - One Card = Last 25 days of Price Data
    - Multiple Cards = Most Recent Price
  - Add and remove tracked cards
  -
- Server
  - Tracking TCGP recent purchase data.
      - Modify card_info.info table columns for TCGP and SF.
  - Config files are called as needed
  - Fetch price and sale data from Scryfall and TCGPlayer, respectively.
  - Automatic setup via `set_up.py`

**To Do:**

  Just check [here](https://github.com/sbyt32/mtg_price_fetcher/discussions/22)

## How it works

### [`set_up.py`](set_up.py)
You should run this first, otherwise nothing will function correctly.<br>



Example `*.log` output
```log
2022-11-23 15:46:13,979 | INFO     | add_remove_db_data.py | Now tracking: Thalia, Guardian of Thraben from Innistrad: Crimson Vow
```

### [Testing (WIP)](tests/)
*This is still a WIP* <br>

Invoke with...
```
pytest --cov=tests/
```

## Libraries
    arrow
    requests
    psycopg[binary]
    fastapi
    hypercorn
    pytest
    httpx
