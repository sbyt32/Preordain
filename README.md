# MTG Price Fetcher
> A simple price and sale fetcher for Magic: The Gathering, powered via Scryfall and TCGPlayer's API and written in Python. Front-end written using SvelteKit


You can use the docker-compose file to deploy the project. However, there will not be any data in the project so your mileage may vary.
<!-- Start the API with...
```
    pip install -r requirements-base.txt
    hypercorn preordain.main:app
``` -->
Written documentation is a WIP. Location is currently [here](docs/api_functions.md). More functions will be added and documented over time.

------------


- [MTG Price Fetcher](#mtg-price-fetcher)
  - [Features](#features)
  - [To Do:](#to-do)
  - [Libraries](#libraries)
    - [Base](#base)
    - [Dev](#dev)
  - [Images (of V1)](#images-of-v1)
    - [Home](#home)
    - [Groups](#groups)
    - [Search](#search)

## Features
*This list is non-exhaustive.*

🟩 indicates a feature fully implemented in both **V1** and **V2**.

🟨 indicates a feature partially implemented, missing some features or characteristics of **V1**.

🟥 indicates a feature not implemented into **V2** that was either fully implemented in **V1** or is new as of **V2**

- API
  - Organize and track personal inventory 🟥
    - Compare current price vs purchase price. 🟥
    - Add, delete, and clear current inventory. 🟥
  - Fetch fresh price data (provided from Scryfall) 🟨
    - See individual card prices 🟨
      - USD, Euro, and Tix, including Day over Day changes 🟨
    - Examine Top gains / losses over USD / Euro / Tix 🟥
  - View and catagorize various cards as different groups 🟥
- Scraper 🟥
  - Automatically scrape Scryfall price data and TCGPlayer sale data 🟥

## To Do:

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
    sqlalchemy
    cachetools
  ### Dev
    flake8
    black
    pytest
    pytest-cov
    pre-commit
    pip-tools


## Images (of V1)

### Home
![home](https://user-images.githubusercontent.com/73682114/227756059-f62f8074-2d80-4c19-b68f-f7df6fc6914b.png)

### Groups
![groups](https://user-images.githubusercontent.com/73682114/227756063-bbe35141-c3e0-496b-be2d-4f6147d927ae.png)
![group page](https://user-images.githubusercontent.com/73682114/227756066-9deac17f-12ea-468e-b031-ff262baadd43.png)
### Search
![search](https://user-images.githubusercontent.com/73682114/227756068-870dd243-cf9e-489a-9233-69be649b255b.png)
