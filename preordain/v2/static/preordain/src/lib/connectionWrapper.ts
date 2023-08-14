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
  Price
}

export interface searchOptions {
  query? : string
  setCode? : string
  collectorNumber? : string
}

function getAPILink(
    route: APIRoutes,
    options:searchOptions
  ) {


  switch (route) {
    case APIRoutes.Search:
      return `info/search/${options.query}`
    case APIRoutes.Price:
      return `price/${options.setCode}/${options.collectorNumber}`
    default:
      break;
  }
}

export async function queryAPI(
  route: APIRoutes,
  options: searchOptions,
  headers: HeadersInit = {'accept': 'application/json'},
  method:string = "GET"
  ) {
  let resp = await fetch(`${get(connectURL)}/v2/${getAPILink(route, options)}`, {
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
