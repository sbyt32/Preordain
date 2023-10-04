

-- -- Database: price_tracker

-- Database: price_tracker

-- DROP DATABASE IF EXISTS price_tracker;

CREATE DATABASE price_tracker_v2
WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    TABLESPACE = pg_default CONNECTION
    LIMIT = -1 IS_TEMPLATE = False;

\c price_tracker

CREATE TABLE IF NOT EXISTS card_key_index (
    scryfall_uri text NOT NULL,
    groups text[],
    tcg_id text,
    tcg_id_etched text,
    new_search boolean DEFAULT true,
    scraper boolean DEFAULT false
);

CREATE SCHEMA IF NOT EXISTS card_information;

-- Card Information
CREATE TABLE IF NOT EXISTS card_information.metadata (
    scryfall_uri text NOT NULL PRIMARY KEY,
    card_name text NOT NULL,
    set_code text NOT NULL,
    collector_number text,
    mana_cost text,
    oracle_text text,
    artist text,
    UNIQUE(scryfall_uri)
);

CREATE TYPE card_information.format_legalities AS ENUM (
        'legal',
        'not_legal',
        'banned',
        'restricted'
);

CREATE TABLE IF NOT EXISTS card_information.formats (
    scryfall_uri text NOT NULL PRIMARY KEY,
    standard card_information.format_legalities NOT NULL,
    historic card_information.format_legalities NOT NULL,
    pioneer card_information.format_legalities NOT NULL,
    modern card_information.format_legalities NOT NULL,
    legacy card_information.format_legalities NOT NULL,
    pauper card_information.format_legalities NOT NULL,
    vintage card_information.format_legalities NOT NULL,
    commander card_information.format_legalities NOT NULL,
    UNIQUE(uniq_id)
);

CREATE INDEX card_formats on card_information.formats using btree (scryfall_uri);

CREATE TABLE IF NOT EXISTS card_information.sets (
    set_code        varchar(12)     NOT NULL PRIMARY KEY,
    set_name        text            NOT NULL,
    release_date    date
);

CREATE INDEX card_sets ON card_information.sets USING btree (set_code);

-- Card Groups? IDK what to name it

-- CREATE SCHEMA IF NOT EXISTS user_;

-- CREATE TABLE IF NOT EXISTS ()

-- Price Data
CREATE SCHEMA IF NOT EXISTS card_price_data;

CREATE TABLE IF NOT EXISTS card_price_data.orders (
    tcg_id      text NOT NULL PRIMARY KEY,
    order_date  timestamptz NOT NULL,
    condition   text        NOT NULL,
    variant     text        NOT NULL,
    qty         smallint    NOT NULL,
    buy_price   float(2)    NOT NULL,
    ship_price  float(2)    NOT NULL
);

CREATE TABLE IF NOT EXISTS card_price_data.price (
    scryfall_uri     text NOT NULL PRIMARY KEY,
    date        date,
    usd         float(2),
    usd_foil    float(2),
    usd_etch    float(2),
    euro        float(2),
    euro_foil   float(2),
    tix         float(2)
);

CREATE INDEX card_price ON card_price_data.price USING btree (scryfall_uri);
CREATE INDEX card_price_date ON card_price_data.price USING btree (date);

-- Event Info
CREATE SCHEMA IF NOT EXISTS event_info;

CREATE TABLE IF NOT EXISTS event_info.metadata (
    event_uri text NOT NULL PRIMARY KEY,
    event_name TEXT NOT NULL,
    event_date date NOT NULL,
    event_type text NOT NULL,
    event_format text NOT NULL
);

CREATE TABLE IF NOT EXISTS event_info.deck_list_metadata (
    event_uri text NOT NULL PRIMARY KEY,
    deck_id   text NOT NULL,
    deck_name text NOT NULL
);

CREATE TABLE IF NOT EXISTS event_info.deck_list (
    deck_id text NOT NULL,
    quantity smallint NOT NULL,
    scryfall_uri TEXT NOT NULL,
    mainboard boolean,
    companion boolean DEFAULT FALSE
);

-- -- DROP DATABASE IF EXISTS price_tracker;

-- CREATE DATABASE price_tracker
-- WITH
--     OWNER = postgres ENCODING = 'UTF8' LC_COLLATE = 'en_US.utf8' LC_CTYPE = 'en_US.utf8' TABLESPACE = pg_default CONNECTION
-- LIMIT = -1 IS_TEMPLATE = False;

-- \c price_tracker


-- CREATE SCHEMA IF NOT EXISTS card_info;

-- DROP TYPE IF EXISTS condition_enum;

-- CREATE TYPE condition_enum AS ENUM (
--         'NM',
--         'LP',
--         'MP',
--         'HP',
--         'DMG',
--         'SEAL'
-- );

-- DROP TYPE IF EXISTS public.variant;

-- CREATE TYPE variant AS ENUM ('Normal', 'Foil', 'Etched');

-- CREATE TABLE
--         IF NOT EXISTS card_info.info (
--                 name varchar(255),
--                 set varchar(12),
--                 id text,
--                 uri text,
--                 tcg_id text,
--                 tcg_id_etch text,
--                 groups text [],
--                 new_search boolean DEFAULT true,
--                 scrape_sales boolean DEFAULT false,
--                 UNIQUE(uri)
-- );

-- CREATE INDEX card_identity ON card_info.info (uri);

-- CREATE TABLE IF NOT EXISTS card_data (
--         uri      text NOT NULL,
--         date     date NOT NULL,
--         usd      float(2),
--         usd_foil float(2),
--         usd_etch float(2),
--         euro float(2),
--         euro_foil float(2),
--         tix float(2)
-- );
-- CREATE INDEX card_identity ON public.card_data USING btree (uri);


-- CREATE TABLE IF NOT EXISTS card_info.sets (
--         set varchar(12) NOT NULL PRIMARY KEY,
--         set_full text NOT NULL,
--         release_date date
-- );

-- CREATE INDEX card_sets ON card_info.sets USING btree (set);

-- CREATE TABLE IF NOT EXISTS card_info.groups (
--         group_name text NOT NULL,
--         description text NOT NULL,
--         banner_uri text NOT NULL,
--         UNIQUE(group_name)
-- );

-- CREATE TABLE IF NOT EXISTS card_data_tcg (
--         order_id varchar NOT NULL,
--         tcg_id text NOT NULL,
--         order_date timestamptz NOT NULL,
--         condition text NOT NULL,
--         variant text NOT NULL,
--         qty smallint NOT NULL,
--         buy_price float(2) NOT NULL,
--         ship_price float(2) NOT NULL,
--         UNIQUE(order_id)
-- );

-- CREATE TABLE IF NOT EXISTS inventory (
--         add_date date,
--         uri text NOT NULL,
--         qty int,
--         buy_price float(2),
--         card_condition text,
--         card_variant text
-- );

-- -- Card Metadata.

-- CREATE TYPE card_info.rarity AS ENUM (
--         'common',
--         'uncommon',
--         'rare',
--         'special',
--         'mythic',
--         'bonus'
-- );

-- CREATE TABLE IF NOT EXISTS card_info.metadata (
--         uri text PRIMARY KEY,
--         rarity card_info.rarity NOT NULL,
--         mana_cost text,
--         oracle_text text,
--         artist text,
--         UNIQUE(uri)
-- );

-- DROP TYPE IF EXISTS card_info.format_legalities;

-- CREATE TYPE card_info.format_legalities AS ENUM (
--         'legal',
--         'not_legal',
--         'banned',
--         'restricted'
-- );

-- CREATE TABLE IF NOT EXISTS card_info.formats (
--         uri text PRIMARY KEY,
--         standard card_info.format_legalities NOT NULL,
--         historic card_info.format_legalities NOT NULL,
--         pioneer card_info.format_legalities NOT NULL,
--         modern card_info.format_legalities NOT NULL,
--         legacy card_info.format_legalities NOT NULL,
--         pauper card_info.format_legalities NOT NULL,
--         vintage card_info.format_legalities NOT NULL,
--         commander card_info.format_legalities NOT NULL,
--         UNIQUE(uri)
-- );

-- CREATE SCHEMA event_data;

-- CREATE TABLE IF NOT EXISTS event_data.events (
--         format text NOT NULL,
--         url text NOT NULL,
--         event_name text NOT NULL,
--         event_date date NOT NULL,
--         event_type text NOT NULL,
--         UNIQUE(url)
-- );
