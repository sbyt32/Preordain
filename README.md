# MTG Price Fetcher
> A simple price and sale fetcher for Magic: The Gathering, powered via Scryfall and TCGPlayer's API and written in Python.

This project contains a group of Python scripts that will allow the user to create a PostgreSQL database, and begin to scrape price data from Scryfall and TCGPlayer. It uses FastAPI to retrieve information from the database and returns in a .json format. 

- [MTG Price Fetcher](#mtg-price-fetcher)
  - [Features](#features)
  - [How it works](#how-it-works)
    - [`set_up.py`](#set_uppy)
      - [`cfg_setup()`](#cfg_setup)
      - [`set_up_db()`](#set_up_db)
    - [`api.py`](#apipy)
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
- Server
    - Manipulate Price Data
    - Consistent import names
- API
    - Refactor router-related data
    - Custom classes for response formats
- Both
    - Custom Exceptions for cleaner errors
    - Update README
    - Testing
- Front-End
    - Exist [Which means now.](https://github.com/sbyt32/price-fetcher-site)

## How it works

### [`set_up.py`](set_up.py)
You should run this first, otherwise nothing will function correctly.<br>
`set_up.py` will first check if the config files exists already, and asks if you want to overwrite the config if so desired. It will then invoke other functions, depending on user input.

#### `cfg_setup()`
If you decide to re/create the config files, `set_up.py` will then call the function `cfg_setup()`. This function is located in the file [`config_setup.py`](scripts/setup_scripts/config_setup.py). 

You will then be prompted to ask if you would like to create the database. This will be checked and performed later in setup.

It will then ask for the host address (default: localhost) of the database, the username and password to use to connect to the database, and the name of the database (default: price_tracker). 

 will then prompt you for tokens to manage access to the database when the FastAPI queries are called. The tokens are...
- Security
  - For general access into the database
- Write
  - For manually adding and removing data in the DB
- Price
  - For accessing large price-related information

#### `set_up_db()`
After token creation, `set_up.py` will then check if the database exists already. If it does, it will then ask if you'd like to recreate the database. If you choose to or if the database does not exist, it will run the function `set_up_db()`, located in the file [`db_setup.py`](scripts/setup_scripts/db_setup.py). 

| Name                 | Type     | Desc                                                                     |
| -------------------- | -------- | ------------------------------------------------------------------------ |
| {database name}      | Database | The name of your database                                                |
| public.card_data     | Table    | public schema, holds card price data. Fetched daily via Scryfall         |
| public.card_data_tcg | Table    | public schema, grabs recent sales from TCGPlayer. Fetched weekly         |
| card_info            | Schema   | A schema to separate the price data and the information that supports it |
| card_info.info       | Table    | card_info table, holds identifiying information formation for cards      |
| card_info.sets       | Table    | card_info table, holds the names of sets and information about them      |
| card_info.groups     | Table    | card_info table, documents card groups                                   |
| condition            | Enum     | Create a set of variables for PostgreSQL, for card condition (US FORMAT) |
| variant              | Enum     | Create a set of variables for PostgreSQL, for card variants              |
| public.inventory     | Table    | public schema, holds the inventory of the user                           |

### [`api.py`](api.py)
`api.py` is the API for the project, run it with [hypercorn](https://pgjones.gitlab.io/hypercorn/). It is also currently the only way to add cards to be tracked at the moment (via the docs + Swagger UI docs).

    hypercorn api:app

Uvicorn might work, but have not tried it out.

Written documentation is a WIP. Location is currently [Here](docs/api_functions.md). More functions will be added and documented over time.

### [`fetch_card_data.py`](fetch_card_data.py)
Two scripts in one! The script will first check if the database exists before continuing. If it does not, it will return an error and not function. Otherwise, it will check if a certain time has elapsed, determined by the variables `PRICE_CHECK` and `SALE_CHECK` within the file.

- `query_price()`
  - Pulls price data from Scryfall. This will then implement those prices into database table `public.card_data`.
  - Set Name and Collector Number info is using [Scryfall](https://scryfall.com/sets)'s format.
  - Fetch this data at least **ONCE A DAY**
- `fetch_tcg_sales()`
  - Pull recent sales from TCGPlayer. These will pull the cards that you are currently tracing. Sale data is stored in `public.card_data_tcg`.
  - Fetch this data **ONCE A WEEK TO EVERY OTHER WEEK**
    - Updating too frequently yields no extra results, and could risk drawing unwanted attention.


### [`logging_details.py`](logging_details.py)
Logging setup, the data will be placed in the folder `logs/`. Not much to it.

Example `*.log` output
```log
2022-11-23 15:46:13,979 | INFO     | add_remove_db_data.py | Now tracking: Thalia, Guardian of Thraben from Innistrad: Crimson Vow
```

### [Testing (WIP)](tests/)
*This is still a WIP* <br>
This program is using Pytest to test. 

Invoke with...
```
pytest tests
```

## Libraries
    arrow
    requests
    psycopg[binary]
    fastapi
    hypercorn
    pytest
    httpx

