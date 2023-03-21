import type { BaseResponse, MultipleCardData } from "../../assets/responses"


// /api/card/{group}
export interface GetCardGroup extends BaseResponse {
    resp: 'card_info',
    info: {
        group_name: string,
        description: string,
        cards_in_group: number
    },
    data: [MultipleCardData]
}

interface TableGroups {
    group_name: string
}

export interface PostGroupsNew extends TableGroups {
    description: string
}

export interface DeleteGroupsDelete extends TableGroups {

}
