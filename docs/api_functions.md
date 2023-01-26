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
    - [`/inventory/`](#inventory)
      - [Responses](#responses-4)
    - [`/inventory/add`](#inventoryadd)
      - [Responses](#responses-5)
    - [`/inventory/delete`](#inventorydelete)
      - [Responses](#responses-6)

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
- Example URL: `localhost:8000/card/search?access={access_token}`
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
- Example URL: `localhost:8000/card/search/dnt?access={access_token}`
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
- Example URL: `localhost:8000/card/search/vow/38?access={access_token}`
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
### `/inventory/`
- Method: GET
- Parameters: `access`
- Example URL: `localhost:8000/inventory?access={access_token}`
- Access Tokens: `access`
Did you know we can also operate as an inventory tracker? If you need to monitor your inventory, here you go! **THIS ONLY WORKS IF YOU ARE ALSO TRACKING THE CARD**
#### Responses
`status:200` Normal operations; Return a card that is in inventory
```json
[
  {
    "Name": "Thalia, Guardian of Thraben",
    "Set": "Innistrad: Crimson Vow",
    "Quantity": 2,
    "Condition": "NM",
    "Variation": "Normal",
    "Avg. Cost": 2
  }
]
```
`status:200` Normal operations; When you have nothing in inventory *OR* you have something in inventory, but are not tracking it.
```json
[]
```

### `/inventory/add`
- Method: POST
- Parameters: `write_access`
- Example URL: `localhost:8000/inventory/add`
- Access Tokens: `write_access`
- **Requires**: .JSON Body
  ```json
  {
    "tcg_id": "string",
    "set": "string",
    "col_num": "string",
    "qty": 0,
    "buy_price": 0,
    "condition": "string",
    "card_variant": "string"
  }  
  ```


Do you need to add cards to your inventory? We can do that! You need either the tcgplayer id *or* the three-letter set code and collector number.

The following are valid **Conditions**:
- 'NM',
- 'LP',
- 'MP',
- 'HP',
- 'DMG',
- 'SEAL'


The following are valid **Card Variants**:
-  'Normal',
-  'Foil',
-  'Etched'


#### Responses
`status:200` Normal operations; Added a card from the set and collector number
```json
  {
    "add_date": "2023-01-26",
    "tcg_id": "240325",
    "qty": 2,
    "buy_price": 20,
    "card_condition": "NM",
    "card_variant": "Normal"
  }
```
`status:500` Internal Server Error 
```
Internal Server Error
```

### `/inventory/delete`
- Method: GET
- Parameters: `write_access`
- Example URL: `localhost:8000/inventory/delete`
- Access Tokens: `write_access`
Not Implemented
#### Responses
`status:200` Normal operations; Not Implemented
```json
null
```

<!-- TODO: Document the function of these groups -->
<!-- ## Fetch Card Prices -->
<!-- ## Card Group -->
<!-- ## Manage Tracked Cards -->

<!-- ? Templates -->
 <!-- 
 ? TEMPLATE FOR EACH FUNCTION, USE THIS AAAA
### `/PATH/TO/STUFF`
- Method: GET
- Parameters: `PARAMETERS`, `AND`, `TOKENS`
- Example URL: `localhost:8000/PATH/TO/{STUFF}`
- Access Tokens: `TOKEN`
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