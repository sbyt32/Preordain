interface BaseErrors {
    resp: string
    status: 200 | 400 | 403 | 404
    info? : {}
    data? : [{}]
}

export interface NotFound extends BaseErrors{
    resp: "no_results"
    status: 404
    info: {
        "message": "No Results found!"
    }
}
