import { connectURL } from "$lib/index"
import { get } from "svelte/store"

export async function database(link:string, headers: HeadersInit = {'accept': 'application/json'}, method:string = "GET") {
  let resp = await fetch(`${get(connectURL)}${link}`, {
    headers,
    method
  })
  if (resp.status == 200) {
    return await resp.json()
  } else {
    // throw new Error(`Status Code: ${resp.status}`);
    console.error(await resp.json())
    console.log("Error!")
  }
}

export enum APIRoutes {
  Search,
  Price,
  Image,
  Card
}

export interface SearchOptions {
  query? : string
  setCode? : string
  collectorNumber? : string
  cardURI?: string
}

function getAPILink(
    route: APIRoutes,
    options: SearchOptions
  ) {


  switch (route) {
    case APIRoutes.Search:
      return `info/search/${options.query}`
    case APIRoutes.Price:
      return `price/${options.setCode}/${options.collectorNumber}`
    case  APIRoutes.Image:
      return `images/${options.cardURI}`
    case APIRoutes.Card:
      return `info/card/${options.cardURI}`
    default:
      break;
  }
}

export async function queryAPI(
  route: APIRoutes,
  options: SearchOptions,
  headers: HeadersInit = {'accept': 'application/json'},
  method: string = "GET"
  ) {
  let resp = await fetch(`${get(connectURL)}/v2/${getAPILink(route, options)}`, {
    headers,
    method
  })
  if (resp.status == 200) {
    if (route == APIRoutes.Image) {
      return resp.url
    } else {
      return await resp.json()
    }
  } else {
    // throw new Error(`Status Code: ${resp.status}`);
    console.error(await resp.json())
    console.log("Error!")
  }
}
