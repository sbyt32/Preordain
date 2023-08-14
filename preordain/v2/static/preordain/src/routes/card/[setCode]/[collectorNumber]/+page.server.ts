import { error } from "@sveltejs/kit"
import { database, queryAPI } from "$lib/connectionWrapper"
import { APIRoutes,  type searchOptions} from "$lib/connectionWrapper"
import type { PageServerLoad } from "./$types"
import type { PriceResponse } from "$lib/responses"

export const load: PageServerLoad = async ({ params }) => {
    let options:searchOptions = {...params}
    const data:PriceResponse[] = await queryAPI(APIRoutes.Price, options);

    if (data) {
        return {price: data};
    }
    throw error(404, 'Not Found')
}
