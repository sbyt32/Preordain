// Check percentage
export function parsePercentage(percent:string) {
    if (percent == null) {
        return ""
    }
    let change = parseFloat(percent)
    let classes = "text-white text-right"
    let emoji = "🤷‍♂️"
    if (change > 0) {
        emoji = "📈 "
        classes = "text-emerald-500 text-right"
    } else if (change < 0) {
        emoji = "📉 "
        classes = "text-rose-500 text-right"
    }
    return `<p class=${classes}  style="font-variant-numeric: tabular-nums" >${emoji}${change}%</p>`
}
