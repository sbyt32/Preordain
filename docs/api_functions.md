# API Functions
This is a compiled list of API functions, how to use them, and expected response formats. If you are not sure what the expected format is, check in here.

- [API Functions](#api-functions)
  - [Test Connection](#test-connection)
    - [`/`](#)
      - [Responses](#responses)
  - [Get Some Card Info](#get-some-card-info)
    - [`/card/search`](#cardsearch)
      - [Responses](#responses-1)
    - [`/card/search/{group}`](#cardsearchgroup)
      - [Responses](#responses-2)
    - [`/card/search/{set}/{col_num}`](#cardsearchsetcol_num)
      - [Responses](#responses-3)
  - [Manage Your Inventory](#manage-your-inventory)
  - [Fetch Card Prices](#fetch-card-prices)
  - [Card Group](#card-group)
  - [Manage Tracked Cards](#manage-tracked-cards)

## Test Connection

This is a testing command to make sure the script is set up correctly. This will check if the `config_files/config.ini` file exists and the database check is set to True. 
### `/`
- Method: GET
- Parameters: None
- Exampl URL: `localhost:8000/`
- Access Tokens: None

#### Responses
`status:200` Normal operation
```json
{
  "resp": "ok",
  "status": 200,
  "message": "The request failed due to being at root. If you're just testing if it works, yeah it works."
}
```
`status:500` Occurs when `set_up.py` is not ran, or if `config_files/config.ini` does not exist / the `dbexists` boolean is set to false
```json
{
    "resp"  :   "error",
    "status":   500,
    "detail":   "Configuration file improperly configured. Script will not function."
}
```
## Get Some Card Info
Want to get some info about some cards? This is where you get them!
### `/card/search`
- Method: GET
- Parameters: `access`
- Example URL: `localhost:8000/card/search`
- Access Tokens: `access`
Returns all the cards that you are tracking, including any groups that card belongs to. This method can be extremely verbose and likely not what you want to be using if you are tracking a large amount of cards.

#### Responses
`status:200` Normal operation, contains cards.
```json
{
  "resp": "card_data",
  "status": 200,
  "data": [
    {
      "name": "Urza, Powerstone Prodigy",
      "set_full": "The Brothers' War",
      "set": "bro",
      "id": "69",
      "groups": null
    },
    {
      "name": "Thalia, Guardian of Thraben",
      "set_full": "Innistrad: Crimson Vow",
      "set": "vow",
      "id": "38",
      "groups": [
        "dnt",
        "white"
      ]
    }
  ]
}
```

### `/card/search/{group}`
- Method: GET
- Parameters: `access`, `group`
- Example URL: `localhost:8000/card/search/dnt`
- Access Tokens: `access`
Care only about a certain group of cards? If you know what the group name of that card is, you can search for those cards here! This will also return the most recent price of those cards, if applicable.

#### Responses
`status:200` Normal Operation, search for a group with cards
```json
[
  {
    "name": "Thalia, Guardian of Thraben",
    "set": "Innistrad: Crimson Vow",
    "last_updated": "2023-01-05",
    "usd": 0.92,
    "usd_foil": 3.05,
    "euro": 0.87,
    "euro_foil": 2.95,
    "tix": 0.17
  },
  {
    "name": "Tithe",
    "set": "Visions",
    "last_updated": "2023-01-05",
    "usd": 24.17,
    "usd_foil": null,
    "euro": 20,
    "euro_foil": null,
    "tix": 0.96
  }
]
```
`status:200` Normal Operation, search for a group that **DOES NOT EXIST**
```json
[
  {}
]
```

### `/card/search/{set}/{col_num}`
- Method: GET
- Parameters: `access`, `set`, `col_number`
- Example URL: `localhost:8000/card/search/vow/38`
- Access Tokens: `access`
If you know what exact card you are looking for, you can recieve that cards information directly! You just need to use the three-letter set code (set) and the collector number (col_num) to get the data. Currently returns internal data.
#### Responses
`status:200` Normal operations; Card exists
```json
{
  "resp": "card_data",
  "status": 200,
  "data": {
    "name": "Thalia, Guardian of Thraben",
    "set": "vow",
    "id": "38",
    "URL": "c9f8b8fb-1cd8-450e-a1fe-892e7a323479"
  }
}
```
`status:404` Database is functioning, the card you are searching for is NOT on the database.
```json
{
  "detail": "This card does not exist on the database!"
}
```

## Manage Your Inventory
## Fetch Card Prices
## Card Group
## Manage Tracked Cards

<!-- ? Templates -->
 <!-- 
 ? TEMPLATE FOR EACH FUNCTION, USE THIS AAAA
    ### `/PATH/TO/STUFF`
    - Method: GET
    - Parameters: `PARAMETERS`, `AND`, `TOKENS`
    - Example URL: `localhost:8000/PATH/TO/{STUFF}
    - Access Tokens: `TOEN`
    PUT A DESCRIPTION IN HERE, MAKE IT CLEAN AND COHERENT
    #### Responses
    `status:200` Normal operations; EXPLAIN WHAT IS CONSIDERED A NORMAL SEARCH, LIKE CARD IN DB OR W/E
    ```json
    {
      "IT": "IS JSON"
    }
    ```
    `status:ERR_CODE` WHEN BAD
    ```json
    {
      "IT": "IS JSON BUT ERROR"
    }
    ```
 -->