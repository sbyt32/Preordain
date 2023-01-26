# Build-your-own-query, TCG Edition
## Payload
```json
{
    "variants": [
        1, // Non-Foil
        2, // Foil
    ],
    "conditions": [
        1, // = Near Mint (NP)
        2, // = Lightly Played (LP)
        3, // = Moderately Played (MP)
        4, // = Heavily Played (HP)
        5, // = Damaged (DMG) 
        6, // = Unopened (SEAL) 
    ],

    "languages": [
        1, // = English   
        2, // = Chinese (Simplified) 
        3, // = Chinese (Traditional) 
        4, // = French   
        5, // = German   
        6, // = Italian   
        7, // = Japanese   
        8, // = Korean  
        9, // = Portuguese   
        10, // = Russian   
        11, // = Spanish   
    ],
    "listingType": "All",
    // Listing Type: 
        // "All"                    = Shows all listings
        // "ListingWithPhotos"      = Shows only listings with photos
        // "ListingWithoutPhotos"   = Shows only listings without photos
    "limit": 25, // 1-25 0 returns 10, 
    "offset":0, // Self Explanatory
}
```

## Result
### **Fetched Card:** Ragavan, Nimble Pilferer (MH2) (Regular)
```json
{
	"previousPage": "Yes",
	"nextPage": "",
	"resultCount": 11, 
	"totalResults": 1786,
	"data": [
		{
			"condition": "Near Mint",                   // Card Condition
			"variant": "Normal",                        // Variant, Foil or Normal. Etched are considered "Foil" in the API
			"language": "English",                      // Language
			"quantity": 1,                              // Quantity
			"title": "Ragavan, Nimble Pilferer",        // Card Name
			"listingType": "ListingWithoutPhotos",      // Does the listing have a Photo?
			"customListingId": "",                      // Idunno 
			"purchasePrice": 66.99,                     // Price it was sold for, not including Tax
			"shippingPrice": 0.0,                       // Shipping price
			"orderDate": "2022-09-22T02:31:47.62+00:00" // Order Date, using ISO 8601
		},
		{
			"condition": "Near Mint",
			"variant": "Normal",
			"language": "English",
			"quantity": 1,
			"title": "Ragavan, Nimble Pilferer",
			"listingType": "ListingWithoutPhotos",
			"customListingId": "",
			"purchasePrice": 59.99,
			"shippingPrice": 4.99,
			"orderDate": "2022-09-22T00:03:49.606+00:00"
		}
	]
}
```

