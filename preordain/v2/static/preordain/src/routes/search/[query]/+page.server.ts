import { error } from "@sveltejs/kit"
import { database } from "$lib/connectionWrapper"
import type { PageServerLoad } from "./$types"


export const load: PageServerLoad =async ({ params }) => {
    const post = await database(`/v2/info/search/${params.query}`);

    if (post) {
        return {post};
    }
    throw error(404, 'Not Found')
}
