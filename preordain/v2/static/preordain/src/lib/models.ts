interface CardMetadata {
    card_name: string
    set_code: string
    collector_number: string
    mana_cost: string
    oracle_text: string
    artist: string
}

enum Legality {
    legal,
    not_legal,
    restricted,
    banned
}

interface CardLegalities {
    standard: Legality
    historic: Legality
    pioneer: Legality
    modern: Legality
    legacy: Legality
    pauper: Legality
    vintage: Legality
    commander: Legality
}
