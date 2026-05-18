import { computed } from "vue"
import { useGameInfoStore } from "../store/gameInfoStore"


export const sortValues = [
	{
		title: "сначала дешевые", 
		value: "cheap"
	},
	{
		title: "сначала дорогие", 
		value: "expensive"
	}
]

const { gameOffers } = useGameInfoStore()

export const availableGameOffersFiltersOptions = {
	stores: computed(() => gameOffers.value.map(offer => ({ title: offer.store, value: offer.store})))
}