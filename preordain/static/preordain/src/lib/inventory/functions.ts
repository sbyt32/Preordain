const verboseConditions = {
    NM: "Near Mint",
    LP: "Lightly Played",
    MP: "Moderately Played",
    HP: "Heavily Played",
    DMG: "Damaged"
}

const verboseVariants = {
    Normal : "Non-Foil",
    Foil : "Foil 🌟",
    Etched : "Etched",
}

export function humanizeConditions(condition:string) {
    return verboseConditions[condition]
}

export function humanizeVariants(variant:string) {
    return verboseVariants[variant]
}
