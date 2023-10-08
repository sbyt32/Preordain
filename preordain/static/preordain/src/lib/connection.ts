// import { connectURL } from "$lib/index"
import { get } from "svelte/store"

export async function database(link:string, headers: HeadersInit = {'accept': 'application/json'}, method:string = "GET") {
  let resp = await fetch(`http://127.0.0.1:8000/${link}`, {
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

export async function fetchImageFromDatabase(uri: string) {
  let resp = await fetch(`http://127.0.0.1:8000/images/${uri}`)

  if (resp.status == 200) {
    return URL.createObjectURL(await resp.blob())
  } else {
    console.log("Error!")
  }
}
