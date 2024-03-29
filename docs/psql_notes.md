# PostgreSQL Notes
The following is a collection of assorted notes and test queries. Some queries may eventually become features in the future.


## SELECT
Get all cards from table where the value is in the array, anywhere.
```postgresql
SELECT * FROM schema_name.table_name WHERE 'value' = ANY (array_col);
```

## INSERT
For adding new data into the table
```postgresql
INSERT INTO schema_name.table_name ('column','name') VALUES ('value','name')
```

### Example
```postgresql
INSERT INTO card_info.info ('id','set') VALUES ('38','vow')
```

## ALTER
For alterting the table structure
```postgresql
ALTER TABLE schema_name.table_name
```

### Add a column
```postgresql
ADD column_name TEXT
```

## UPDATE
For changing rows in the table
```postgresql
UPDATE schema_name.table_name SET column_name = 'value'
```
Remove array data
```postgresql
UPDATE schema_name.table_name SET column_name = array_remove(column_name, 'value_to_remove')
```


Assorted Queries
===========================
### Retrieve Total Number of Sales
```postgres
SELECT
    DATE_TRUNC('day', order_date) AS "day",
    COUNT("order_date") AS "number_of_sales"
FROM
    card_data_tcg
GROUP BY
    DATE_TRUNC('day', order_date)
ORDER BY
    day ASC;
```
### *sales of one card, avg sale price*

```postgres
SELECT
    info.name,
    info.set,
    info.id,
    DATE_TRUNC('day', order_date) AS day,
    COUNT("order_date") AS "number_of_sales",
    (SUM(buy_price * qty) / COUNT("order_date"))::numeric(10,2) as "avg_cost"
FROM
    card_data_tcg
JOIN card_info.info AS info
    ON info.tcg_id = card_data_tcg.tcg_id
WHERE info.set = 'vow'
    AND info.id = '38'
    AND condition = 'Near Mint'
    AND variant = 'Normal'
GROUP BY
    DATE_TRUNC('day', order_date), info.name, info.set,info.id
ORDER BY
    day ASC;
```

```
JOIN (
    SELECT
        tcg_id,
        DATE_TRUNC('day', order_date) AS "day",
        COUNT("order_date") AS "number_of_sales"
    FROM
        card_data_tcg
    WHERE condition = 'Near Mint'
        AND variant = 'Normal'
        AND tcg_id = '252859'
    GROUP BY
        DATE_TRUNC('day', order_date), tcg_id
    ORDER BY
        day ASC
) AS day_total
    ON info.tcg_id = day_total.tcg_id
```
### Merge both tables together
```POSTGRESQL
SELECT
    tb1.name as "Name",
    tb3.set_full as "Set Name (Full)",
    tb2.date as "Date",
    tb2.usd "USD",
    tb2.usd_foil "USD (Foil)",
    tb2.euro "Euro",
    tb2.euro_foil "Euro (Foil)",
    tb2.tix "MTGO Tix"
    FROM card_info.info tb1
    LEFT    JOIN (
            SELECT *
            FROM    dblink('dbname=price_tracker', 'SELECT * FROM card_data')
            AS      tb2(
                        set varchar(12),
                        id text,
                        date date,
                        usd float(2),
                        usd_foil float(2),
                        euro float(2),
                        euro_foil float(2),
                        tix float(2)
                    )
    ) AS tb2
        ON  tb2.id = tb1.id
        AND tb2.set = tb1.set
    JOIN card_info.sets AS tb3
        ON tb2.set = tb3.set
    WHERE tb1.set = 'mh2' AND tb1.id = '138'
    ORDER BY tb2.date DESC;
```

### Get the price of cards while also returning the amount of sales of that card
```postgres
SELECT
        card_info.name as "Name",
        set_info.set_full as "Set Name (Full)",
        price_info.date as "Date",
        price_info.usd "USD",
        price_info.usd_foil "USD (Foil)",
        price_info.euro "Euro",
        price_info.euro_foil "Euro (Foil)",
        price_info.tix "MTGO Tix",
        COALESCE(sale_total.number_of_sales, 0) "Number of Sales"
FROM card_info.info card_info
LEFT    JOIN (
        SELECT *
        FROM    dblink('dbname=price_tracker', 'SELECT * FROM card_data')
        AS      price_info(
                    set varchar(12),
                    id text,
                    date date,
                    usd float(2),
                    usd_foil float(2),
                    euro float(2),
                    euro_foil float(2),
                    tix float(2)
                )
) AS price_info
    ON  price_info.id = card_info.id
    AND price_info.set = card_info.set
LEFT    JOIN (
        SELECT
            DATE_TRUNC('day', order_date) AS "day", COUNT("order_date") AS "number_of_sales", tcg_id
        FROM
            card_data_tcg
        GROUP BY
            DATE_TRUNC('day', order_date),
            tcg_id
) AS sale_total
    ON sale_total.tcg_id = card_info.tcg_id
    AND sale_total.day = price_info.date
JOIN card_info.sets AS set_info
    ON set_info.set = card_info.set
WHERE card_info.name = 'Circle of Protection: Black'
ORDER BY Date
    DESC
```

### Get list of all groups in use
```postgres
SELECT
    DISTINCT(group_in_use) AS "group",
    groups.description
FROM (
    SELECT
        UNNEST(groups)
    FROM
    card_info.info
    ) AS a(group_in_use)
JOIN card_info.groups AS groups
    ON groups.group_name = group_in_use
```

### Select the most recent price points
```postgres
SELECT
    info.name,
    info.set_full,
    info.id,
    info.maxDate as "date",
    price.usd,
    price.usd_foil,
    price.euro,
    price.euro_foil,
    price.tix
FROM card_data price
JOIN (
    SELECT
        info.name,
        info.set,
        sets.set_full,
        info.id,
        MAX(date) as maxDate
    FROM card_data
    JOIN card_info.info as info
        ON info.set = card_data.set
        AND info.id = card_data.id
    JOIN card_info.sets as sets
        ON sets.set = card_data.set
    GROUP BY sets.set_full, info.id, info.name, info.set
    ) info
ON price.id = info.id
    AND price.set = info.set
    AND price.date = info.maxDate

```

```postgres
SELECT
    info.name,
    info.set_full,

```

### Find a card in the db, case-insensitive
```postgresql
select * from card_info.info where lower(card_info.info.name) LIKE lower('%Thalia%');
```

### ugliest sql command on the market, gets average cost change
```postgresql
        SELECT
            info.name,
            info.set,
            info.id,
            DATE_TRUNC('day', order_date) AS day,
            COUNT("order_date") AS "number_of_sales",
            (SUM(buy_price * qty) / COUNT("order_date"))::numeric(10,2) as "avg_cost",
            CASE WHEN
                LAG (
                    (SUM(buy_price * qty) / COUNT("order_date"))::numeric(10,2), 1)
                    OVER
                    (ORDER BY DATE_TRUNC('day',order_date))
                            is NULL THEN 0
            ELSE
                ROUND (
                    100.0 *
                        (
                        (SUM(buy_price * qty) / COUNT("order_date"))::numeric(10,2) - LAG((SUM(buy_price * qty) / COUNT("order_date"))::numeric(10,2),1)
                        OVER
                        (ORDER BY DATE_TRUNC('day',order_date))
                        )
                        /
                        LAG((SUM(buy_price * qty) / COUNT("order_date"))::numeric(10,2),1)
                        OVER
                        (ORDER BY DATE_TRUNC('day',order_date)),2)
            END || '%%'
            AS daily_delta
        FROM
            card_data_tcg
        JOIN card_info.info AS info
            ON info.tcg_id = card_data_tcg.tcg_id
        WHERE info.set = 'vow'
            AND info.id = '38'
            AND condition = 'Near Mint'
            AND variant = 'Normal'
        GROUP BY
            DATE_TRUNC('day', order_date), info.name, info.set,info.id
        ORDER BY
            day ASC
        LIMIT 62
```
above but get sale cnt
```postgresql
        SELECT
            info.name,
            info.set,
            info.id,
            DATE_TRUNC('day', order_date) AS day,
            COUNT("order_date") AS "number_of_sales",
            (SUM(buy_price * qty) / COUNT("order_date"))::numeric(10,2) as "avg_cost",
            CASE WHEN
                LAG(COUNT("order_date"),1) OVER (ORDER BY DATE_TRUNC('day',order_date)) is NULL THEN 0
            ELSE
                ROUND (
                    100.0 * (
                        COUNT("order_date") - LAG(COUNT("order_date"),1)
                        OVER (ORDER BY DATE_TRUNC('day',order_date))
                    ) / LAG(COUNT("order_date"),1)
                        OVER (ORDER BY DATE_TRUNC('day',order_date)),2)
            END || '%%'
            AS daily_delta
        FROM
            card_data_tcg
        JOIN card_info.info AS info
            ON info.tcg_id = card_data_tcg.tcg_id
        WHERE info.set = %s
            AND info.id = %s
            AND condition = 'Near Mint'
            AND variant = 'Normal'
        GROUP BY
            DATE_TRUNC('day', order_date), info.name, info.set,info.id
        ORDER BY
            day ASC
        LIMIT 62
```
```
        SELECT
            card_info.info.name,
            card_info.sets.set,
            card_info.sets.set_full,
            card_info.info.id,
            date,
            usd,
            ROUND ( 100.0 * (change.usd_ct::numeric - change.usd_yesterday::numeric) / change.usd_yesterday::numeric, 2) || '%' AS usd_change,
            usd_foil,
            ROUND ( 100.0 * (change.usd_foil_ct::numeric - change.usd_foil_yesterday::numeric) / change.usd_foil_yesterday::numeric, 2) || '%' AS usd_foil_change,
            euro,
            ROUND ( 100.0 * (change.euro_ct::numeric - change.euro_yesterday::numeric) / change.euro_yesterday::numeric, 2) || '%' AS euro_change,
            euro_foil,
            ROUND ( 100.0 * (change.euro_foil_ct::numeric - change.euro_foil_yesterday::numeric) / change.euro_foil_yesterday::numeric, 2) || '%' AS euro_foil_change,
            tix,
            ROUND ( 100.0 * (change.tix_ct::numeric - change.tix_yesterday::numeric) / change.tix_yesterday::numeric, 2) || '%' AS tix_change
        FROM card_data
        JOIN card_info.info
            ON card_data.set = card_info.info.set
            AND card_data.id = card_info.info.id
        JOIN card_info.sets
            ON card_data.set = card_info.sets.set
        JOIN
            (
                SELECT
                    date AS dt,
                    set,
                    id,
                    usd AS usd_ct,
                    lag(usd, 1) over (partition by set, id order by date(date)) AS usd_yesterday,
                    usd_foil AS usd_foil_ct,
                    lag(usd_foil, 1) over (partition by set, id order by date(date)) AS usd_foil_yesterday,
                    euro AS euro_ct,
                    lag(euro, 1) over (partition by set, id order by date(date)) AS euro_yesterday,
                    euro_foil AS euro_foil_ct,
                    lag(euro_foil, 1) over (partition by set, id order by date(date)) AS euro_foil_yesterday,
                    tix AS tix_ct,
                    lag(tix, 1) over (partition by set, id order by date(date)) AS tix_yesterday
                FROM card_data
                GROUP BY set, id, date, usd, usd_foil, euro, euro_foil, tix ORDER BY date DESC
            ) AS change
        ON change.dt = card_data.date
        AND change.set = card_data.set
        AND change.id = card_data.id
        ORDER BY date DESC
        LIMIT %s
```



""" 2500ms query. Get d/d changes of cards in group.
EXPLAIN ANALYZE
        SELECT
            DISTINCT ON (info.name, info.id, info.set) "name",
            info.set,
            sets.set_full,
            info.id,
            prices.date "last_updated",
            prices.usd,
            prices.usd_foil,
            prices.euro,
            prices.euro_foil,
            prices.tix,
            usd_change,
            usd_foil_change,
            euro_change,
            euro_foil_change,
            tix_change
        FROM card_info.info AS "info"
        JOIN card_info.sets AS "sets"
            ON info.set = sets.set
        JOIN
            (
                SELECT
                    prices.date,
                    prices.uri,
                    prices.usd,
                    prices.usd_foil,
                    prices.euro,
                    prices.euro_foil,
                    prices.tix,
                    ROUND ( 100.0 *
                        (usd::numeric - lag(usd, 1) over (partition by uri order by date(date))::numeric)
                        /
                        lag(usd, 1) over (partition by uri order by date(date))::numeric
                    , 2) AS "usd_change",
                    ROUND ( 100.0 *
                        (usd_foil::numeric - lag(usd_foil, 1) over (partition by uri order by date(date))::numeric)
                        /
                        lag(usd_foil, 1) over (partition by uri order by date(date))::numeric
                    , 2) AS "usd_foil_change",
                    ROUND ( 100.0 *
                        (euro::numeric - lag(euro, 1) over (partition by uri order by date(date))::numeric)
                        /
                        lag(euro, 1) over (partition by uri order by date(date))::numeric
                    , 2) AS "euro_change",
                    ROUND ( 100.0 *
                        (euro_foil::numeric - lag(euro_foil, 1) over (partition by uri order by date(date))::numeric)
                        /
                        lag(euro_foil, 1) over (partition by uri order by date(date))::numeric
                    , 2) AS "euro_foil_change",
                    ROUND ( 100.0 *
                        (tix::numeric - lag(tix, 1) over (partition by uri order by date(date))::numeric)
                        /
                        lag(tix, 1) over (partition by uri order by date(date))::numeric
                    , 2) AS "tix_change"
                FROM
                    card_data as "prices"
                WHERE prices.date = (SELECT MAX(date) as last_update from card_data)
                OR date = (SELECT lag(date, -1) over (order by date desc) from card_data GROUP BY date LIMIT 1)
            ) AS "prices"
        ON prices.uri = info.uri
        WHERE 'dnt' = ANY (info.groups)
        ORDER BY
            info.name,
            info.id,
            info.set,
            prices.date DESC
;
"""
