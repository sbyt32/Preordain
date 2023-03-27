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
