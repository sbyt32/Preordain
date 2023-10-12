import { error } from "@sveltejs/kit"
import { database, queryAPI } from "$lib/connectionWrapper"
import { APIRoutes,  type searchOptions} from "$lib/connectionWrapper"
import type { PageServerLoad } from "./$types"


export const load: PageServerLoad = async ({ params }) => {
    let options:searchOptions = {...params}
    const data = await queryAPI(APIRoutes.Search, options);

    if (data) {
        return {post: data};
    }
    throw error(404, 'Not Found')
}
