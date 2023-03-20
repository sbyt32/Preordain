export async function database(link:string, header?: Object) {
    let resp = await fetch(link, {
      headers: {
        'accept': 'appplication/json'
      },
      method: 'GET',
    })
    if (resp.status == 200) {
      let data = await resp.json()
      return data
    }
  }
