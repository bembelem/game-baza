import type { GameOffersFilters } from "../filters/gameOffersFilters"
import type { Offer } from "@/entities/offer/model/Offer"


function matchesPriceFilter(value: number, filterValue: GameOffersFilters["price"]["value"]) {
	if (!filterValue) return true

	const matchesMin = value >= filterValue[0]
	const matchesMax = filterValue[1] ? value <= filterValue[1] : true 
	
	return matchesMin && matchesMax
}


export const useGameOffersFiltered = (
	offers: Offer[],
	gameOffersFilters: Partial<GameOffersFilters>
) => {
	const {sort, ...filters} = gameOffersFilters

	const offersFiltered = offers.filter((offer) => {
		if (filters.price) {
			if (!matchesPriceFilter(offer.price_discount, filters.price.value)) return false
		}
		if (filters.stores?.length) {
			if (!filters.stores.map(store => store.value).includes(offer.store)) return false
		}

		return true
	})
	
	const offersSorted = offersFiltered.sort((a, b) => {
		if (!sort) return 0

		if (sort.value == "cheap") {
			return a.price_discount - b.price_discount
		}
			
		if (sort.value == "expensive") {
			return b.price_discount - a.price_discount
		}

		return 0
	})

	return offersSorted
}