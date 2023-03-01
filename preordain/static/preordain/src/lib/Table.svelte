<script context="module" lang="ts">
    export interface ResponseData {
        name: String
        set: String
        id: String
        usd: Number
        usd_foil: Number
        euro: Number
        euro_foil: Number
        tix: Number
    }
    export let header = ["Name","Set","Collector No.","USD","USD (Foil)","Euro","Euro (Foil)","TIX"]
</script>

<script lang="ts">
    import type { GetCard } from "../assets/responses";
    export let data: GetCard

    function ParseData(data:GetCard): Array<ResponseData> {
        let card_data = data.data
        let resp = []
        for (let i = 0; i < card_data.length; i++) {
            const card_info = card_data[i]
            let response_data = {
                "Name": card_info.name,
                "Set": card_info.set_full,
                "Collector No.": card_info.id,
                "USD": card_info.prices.usd,
                "USD (Foil)": card_info.prices.usd_foil,
                "Euro": card_info.prices.euro,
                "Euro (Foil)": card_info.prices.euro_foil,
                "TIX": card_info.prices.tix,
            }
            resp.push(response_data)
        }
        return resp
    }

    function parseCurrency(price:number | string, currency:string) {
        if (typeof price == "string") {
            return price
        }

        if (currency.toLowerCase().includes("usd")) {
            let stuff = new Intl.NumberFormat("en-US", {style: 'currency', currency: 'USD'}).format(price)
            return stuff
        } else if (currency.toLowerCase().includes("euro")) {
            let stuff = new Intl.NumberFormat("de-DE", {style: 'currency', currency: 'EUR'}).format(price)
            return stuff
        } else if (currency.toLowerCase().includes("tix")) {
            if (!price === null) {
                return `${price} TIX`
            }
            return `0 TIX`
        }
    }

    function parseRow(value: string | number, header: string) {
        if (header === "Name") {
            return  `<th scope="row" class="px-6 py-4 font-medium text-gray-900 dark:text-white">
                        ${value}
                    </th>`
        } else {
            return `<td class="px-6 py-4">
                        ${parseCurrency(value, header)}
            </td>`
        }
    }
</script>

    <!-- max-h-[{((1/4)*100).toFixed(0)}%] -->
<!-- <div class="relative"> -->
    <div class="shadow-md overflow-y-auto overflow-x-hidden sm:rounded-lg max-h-[25%]">
        <table class="w-full text-sm text-left table">
            <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                <tr>
                    {#each header as titles}
                    <th scope="col" class="px-6 py-3">
                        {titles}
                    </th>
                    {/each}

                </tr>
            </thead>
            <tbody>
                {#each ParseData(data) as card_data}
                <tr class="bg-white text-gray-200 dark:bg-gray-800 dark:border-gray-700">
                        {#each header as data_type}
                                {@html parseRow(card_data[data_type], data_type)}
                        {/each}
                </tr>
                {/each}
            </tbody>
        </table>
    </div>
<!-- </div> -->
