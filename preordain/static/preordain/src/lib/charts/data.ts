export {}
// import type { GetPriceSingle } from "../../assets/responses";

// function parsePriceData(price_data:GetPriceSingle) {
//     let labels = []
//     let datasets = [
//         {
//             label: "USD",
//             borderColor: shopInfo[0].colors.rgb.store,
//             backgroundColor: 'rgba(77,124,15, .5)',
//             data: []
//         },
//         {
//             label: "USD (Foil)",
//             borderColor: 'rgb(255, 99, 132)', // To Update
//             data: []
//         },
//         {
//             label: "Euro",
//             borderColor:  shopInfo[1].colors.rgb.store,
//             backgroundColor: 'rgba(2, 132, 199, .5)',
//             data: []
//         },
//         {
//             label: "Euro (Foil)",
//             borderColor: 'rgb(255, 99, 132)', // To Update
//             data: []
//         },
//         {
//             label: "Tickets",
//             borderColor: shopInfo[2].colors.rgb.store,
//             data: []
//         },
//     ]



//     for (let i = 0; i < price_data.prices.length; i++) {
//             labels.push(price_data.prices[i].date);
//             datasets[0].data.push(price_data.prices[i].usd)
//             datasets[1].data.push(price_data.prices[i].usd_foil)
//             datasets[2].data.push(price_data.prices[i].euro)
//             datasets[3].data.push(price_data.prices[i].euro_foil)
//             datasets[4].data.push(price_data.prices[i].tix)
//     }

//     for (let i = 0; i < datasets.length; i++) {
//         if (!datasets[i].data.length == 0 ) {
//             datasets[i] = {
//                 ...datasets[i],
//                 ...chart_shit
//         }
//         }
//     }

//     return {labels,datasets}
// }
