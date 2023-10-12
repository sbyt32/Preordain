import { error } from "@sveltejs/kit"
import { database, queryAPI } from "$lib/connectionWrapper"
import { APIRoutes,  type searchOptions} from "$lib/connectionWrapper"
import type { PageServerLoad } from "./$types"
import type { PriceResponse } from "$lib/responses"

interface ChartPrice {
    Date: Date
    Type: string
    Currency: string
    Price: string | number | null
}

export const load: PageServerLoad = async ({ params }) => {
    const data:PriceResponse[] = await queryAPI(APIRoutes.Price, {...params});
    let chartData:ChartPrice[] = []

    if (data) {
        return {
            price: data,
            chartData: data.forEach(e => {
                let currentDate = new Date(e.date)
                chartData.push(
                    {"Date": currentDate, "Type": "USD", "Currency": "USD", "Price": e.prices.usd}
                )
            })
        };
    }
    throw error(404, 'Not Found')
}

// export const ssr = false
// export const prerender = true
