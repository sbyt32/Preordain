// export {}
import type { GetPriceSingle } from "../../assets/responses";

export function parsePriceData(price_data:GetPriceSingle) {
    const chart_stuff = {
    }
    let items = price_data.data
    let labels = []
    let datasets = [
        {
            label: "USD",
            borderColor: "rgb(77, 124, 15)",
            backgroundColor: 'rgba(77,124,15, .5)',
            data: []
        },
        {
            label: "USD (Foil)",
            borderColor: 'rgb(255, 99, 132)', // To Update
            data: []
        },
        {
            label: "Euro",
            borderColor:  "rgb(2 132 199)",
            backgroundColor: 'rgba(2, 132, 199, .5)',
            data: []
        },
        {
            label: "Euro (Foil)",
            borderColor: 'rgb(255, 99, 132)', // To Update
            data: []
        },
        {
            label: "Tickets",
            borderColor: "rgb(234 88 12)",
            data: []
        },
    ]

    for (let i = 0; i < items.prices.reverse().length; i++) {
            labels.push(items.prices[i].date);
            datasets[0].data.push(items.prices[i].usd)
            datasets[1].data.push(items.prices[i].usd_foil)
            datasets[2].data.push(items.prices[i].euro)
            datasets[3].data.push(items.prices[i].euro_foil)
            datasets[4].data.push(items.prices[i].tix)
    }

    for (let i = 0; i < datasets.length; i++) {
        if (datasets[i].data.length > 0) {
            datasets[i] = {
                ...datasets[i],
                ...chart_stuff
        }
        }
    }

    console.log({labels, datasets});

    return {labels,datasets}
}
