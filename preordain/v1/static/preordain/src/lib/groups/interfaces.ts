import type { BaseResponse, MultipleCardData, PriceData } from "../../assets/responses"
import type { BaseCardData } from "../../assets/interfaces"

// /api/card/{group}
export interface GetCardGroupInfo {
    group_name: string,
    description: string,
    qty: number
}

export interface GroupCardData extends BaseCardData{
    uri: string
    last_updated: string
    prices: PriceData
}

export interface GetCardGroup extends BaseResponse {
    resp: 'group_info'
    info: GetCardGroupInfo
    data: GroupCardData[]
}

interface TableGroups {
    group_name: string
}

export interface PostGroupsNew extends TableGroups {
    description: string
}

export interface DeleteGroupsDelete extends TableGroups {

}
