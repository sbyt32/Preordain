import { error } from "@sveltejs/kit"

import { queryAPI, APIRoutes } from "$lib/connectionWrapper"
import type { PageServerLoad } from "./$types"
import type { PriceResponse } from "$lib/responses"

//

export const load: PageServerLoad = async ({ params }) => {
    const priceData:PriceResponse[] = await queryAPI(APIRoutes.Price, {...params});
    // TODO: create helper query to get the card uri from the params.
    const imgData = await queryAPI(APIRoutes.Image, {cardURI:"a211d505-4d40-4914-a9da-220770d6ddbc"})
    const cardData = await queryAPI(APIRoutes.Card, {cardURI:"a211d505-4d40-4914-a9da-220770d6ddbc"})


    if (priceData) {
        return {
            price: priceData,
            image: imgData,
            card: cardData
            // chartData: chartData
        };
    }
    throw error(404, 'Not Found')
}
export const ssr = false
