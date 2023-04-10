-- Database: price_tracker

-- DROP DATABASE IF EXISTS price_tracker;

CREATE DATABASE price_tracker
WITH
    OWNER = postgres ENCODING = 'UTF8' LC_COLLATE = 'en_US.utf8' LC_CTYPE = 'en_US.utf8' TABLESPACE = pg_default CONNECTION
LIMIT = -1 IS_TEMPLATE = False;

\c price_tracker



CREATE SCHEMA IF NOT EXISTS card_info;

DROP TYPE IF EXISTS condition_enum;

CREATE TYPE condition_enum AS ENUM (
        'NM',
        'LP',
        'MP',
        'HP',
        'DMG',
        'SEAL'
);

DROP TYPE IF EXISTS public.variant;

CREATE TYPE variant AS ENUM ('Normal', 'Foil', 'Etched');

CREATE TABLE
        IF NOT EXISTS card_info.info (
                name varchar(255),
                set varchar(12),
                id text,
                uri text,
                tcg_id text,
                tcg_id_etch text,
                groups text [],
                new_search boolean DEFAULT true,
                scrape_sales boolean DEFAULT false,
                UNIQUE(uri)
);

CREATE INDEX card_identity ON card_info.info (uri);

CREATE TABLE IF NOT EXISTS card_data (
        uri      text NOT NULL,
        date     date NOT NULL,
        usd      float(2),
        usd_foil float(2),
        usd_etch float(2),
        euro float(2),
        euro_foil float(2),
        tix float(2)
);
CREATE INDEX card_identity ON public.card_data USING btree (uri);


CREATE TABLE IF NOT EXISTS card_info.sets (
        set varchar(12) NOT NULL PRIMARY KEY,
        set_full text NOT NULL,
        release_date date
);

CREATE INDEX card_sets ON card_info.sets USING btree (set);

CREATE TABLE IF NOT EXISTS card_info.groups (
        group_name text NOT NULL,
        description text NOT NULL,
        UNIQUE(group_name)
);

CREATE TABLE IF NOT EXISTS card_data_tcg (
        order_id varchar NOT NULL,
        tcg_id text NOT NULL,
        order_date timestamptz NOT NULL,
        condition text NOT NULL,
        variant text NOT NULL,
        qty smallint NOT NULL,
        buy_price float(2) NOT NULL,
        ship_price float(2) NOT NULL,
        UNIQUE(order_id)
);

CREATE TABLE IF NOT EXISTS inventory (
        add_date date,
        uri text NOT NULL,
        qty int,
        buy_price float(2),
        card_condition text,
        card_variant text
);

-- Card Metadata.

CREATE TYPE card_info.rarity AS ENUM (
        'common',
        'uncommon',
        'rare',
        'special',
        'mythic',
        'bonus'
);

CREATE TABLE IF NOT EXISTS card_info.metadata (
        uri text PRIMARY KEY,
        rarity card_info.rarity NOT NULL,
        mana_cost text,
        oracle_text text,
        artist text,
        UNIQUE(uri)
);

DROP TYPE IF EXISTS card_info.format_legalities;

CREATE TYPE card_info.format_legalities AS ENUM (
        'legal',
        'not_legal',
        'banned',
        'restricted'
);

CREATE TABLE IF NOT EXISTS card_info.formats (
        uri text PRIMARY KEY,
        standard card_info.format_legalities NOT NULL,
        historic card_info.format_legalities NOT NULL,
        pioneer card_info.format_legalities NOT NULL,
        modern card_info.format_legalities NOT NULL,
        legacy card_info.format_legalities NOT NULL,
        pauper card_info.format_legalities NOT NULL,
        vintage card_info.format_legalities NOT NULL,
        commander card_info.format_legalities NOT NULL,
        UNIQUE(uri)
);
