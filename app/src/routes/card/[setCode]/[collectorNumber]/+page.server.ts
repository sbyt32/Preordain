import { error } from "@sveltejs/kit"
// import * as d3 from "d3"
// import * as Plot from '@observablehq/plot'
import { database, queryAPI } from "$lib/connectionWrapper"
import { APIRoutes} from "$lib/connectionWrapper"
import type { PageServerLoad } from "./$types"
import type { PriceResponse } from "$lib/responses"

interface ChartPrice {
    Date: Date
    Type: string
    Currency: string
    Price: string | number | null
}

export const load: PageServerLoad = async ({ params }) => {
    let data:PriceResponse[] = await queryAPI(APIRoutes.Price, {...params});

    // let chartData:ChartPrice[] = []

    // data.forEach(e => {
    //     let currentDate = new Date(e.date)
    //     chartData.push(
    //         {"Date": currentDate, "Type": "USD", "Currency": "USD", "Price": e.prices.usd},
    //         {"Date": currentDate, "Type": "USD", "Currency": "USD", "Price": e.prices.usd_foil}
    //         )
    // })

    // const plot = Plot.plot({
    //     // height: window.screenY,
    //     width: 1920,
    //     // margin: 32,

    //     color: {legend: true},
    //     // style: "overflow: visible; font-size: 13px;",
    //     // y: {grid: true, label: "Price", tickFormat: d3.format("$,.2f") },
    //     marks: [
    //         Plot.ruleY([0]),
    //         Plot.axisX({ticks:"week"}),
    //         Plot.gridX({ticks: "month", strokeWidth: 2, stroke: "blue", strokeOpacity: .2}),
    //         Plot.lineY(chartData, {x: "Date", y: "Price", stroke: "Type", strokeWidth: 2}),
    //         // Plot.text(chartData, Plot.selectFirst({x: "Date", y: "Price", z: "Type", text: "Type", textAnchor:"start", dx: 3})),

    //         // Plot.crosshair(chartData, {x: "Date", y: "Price"}),
    //         // Plot.tip(chartData, Plot.pointerX(
    //         //     {x: 'Date', y: "Price", channels: {Date: "Date", Currency: "Currency", Price: "Price" }}
    //         // ))
    //     ],
    //     document
    // }).innerHTML;


    if (data) {
        return {
            price: data
            // chartData: chartData
        };
    }
    throw error(404, 'Not Found')
}
export const ssr = false
// export const prerender = true

// import * as Plot from '@observablehq/plot';
// import type { PageServerLoad } from './$types';
// // @ts-ignore
// import { JSDOM } from 'jsdom';

// const { document } = new JSDOM().window;

// // /** @type {import('./$types').PageServerLoad} */
// export async function load() {
//   const plot = Plot.plot({
//     marks: [
//       Plot.rectY(
//         { length: 10000 },
//         Plot.binX({ y: "count" }, { x: Math.random })
//       )
//     ],
//     document
//   }).outerHTML;

//   return {
//     plot
//   };
// }
