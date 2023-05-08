// Check percentage
export function parsePercentage(percent:string) {
    if (percent === null) {
        return ""
    }
    let change = parseFloat(percent)
    if (Number.isNaN(change)) {
        return "<p class='invisible'>empty</p>"
    }
    let classes = "text-white tabular-nums"
    let emoji = "🤷‍♂️"
    if (change > 0) {
        emoji = "📈  "
        classes = "text-emerald-500 tabular-nums"
    } else if (change < 0) {
        emoji = "📉"
        classes = "text-rose-500 tabular-nums"
    }
    return `<p class="${classes}">${emoji}${change}%</p>`
}

// Parse Oracle Text

export function parseOracleText(oracle: string): string {
    let respHTML = ""
    let textLines = oracle.split("\n")
    textLines.forEach(e => {
        respHTML += `<li class="ml-8 leading-relaxed list-disc">${e}</li>`
    });
    return `
        <div class="text-left font-semibold">Oracle:
            <ul class="list-inside font-normal">
                ${respHTML}
            </ul>
        </div>
        `
}

export function parseFormatLegality(format: string): string{
    switch (format) {
        case "legal":
            return `<span class="bg-green-600/80 text-black border-2 border-black rounded-xl text-lg font-normal">
                Legal
            </span>`
        case "restricted":
            return `<span class="bg-orange-500   text-white border-2 border-black rounded-xl text-lg font-normal">
                Restricted
            </span>`
        case "banned":
            return `<span class="bg-red-500/80   text-white border-2 border-black rounded-xl text-lg font-normal">
                Banned
            </span>`
        default:
            return `<span class="bg-gray-500     text-black border-2 border-black rounded-xl text-lg font-normal">
                Not Legal
            </span>`
    }
}

export function parseCurrency(price:number | string, currency:string) {
    // Checks
    if (typeof price === "string") {
        return price
    } else if (price === null) {
        return `N/A`
    }

    if (currency.toLowerCase().includes("usd")) {
        let stuff = new Intl.NumberFormat("en-US", {style: 'currency', currency: 'USD'}).format(price)
        return stuff
    } else if (currency.toLowerCase().includes("euro")) {
        let stuff = new Intl.NumberFormat("de-DE", {style: 'currency', currency: 'EUR'}).format(price)
        return stuff
    } else {
        return `${price} TIX`
    }
}
