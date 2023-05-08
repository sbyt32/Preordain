import { connectURL } from "../assets/stores"
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
// else
// switch (resp.status) {
//   case 404:
//       return
//   case 201:
//       return await resp.json()
//   default:
//     return await resp.json()
// }
