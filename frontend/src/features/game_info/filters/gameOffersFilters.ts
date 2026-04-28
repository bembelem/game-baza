import type { SelectorValue, FiltersDefinition } from "@/shared/interface/Filters"
import { sortValues } from "./gameOffersFiltersData"
import { ResetBehavior } from "@/shared/interface/Filters"
import { priceValues } from "@/shared/data/filtersValues"
import { useFilters } from "@/shared/lib/useFilters"
import { useFiltersOptions } from "@/shared/lib/useFiltersOptions"
import { availableGameOffersFiltersOptions } from "./gameOffersFiltersData"


export interface GameOffersFilters {
	sort: SelectorValue<string>,
	stores: SelectorValue<string>[],
	price: SelectorValue<[number, number | undefined] | undefined>
}

type GameOffersFiltersDefinition = FiltersDefinition<GameOffersFilters>


export const gameOffersFiltersDefinition: GameOffersFiltersDefinition = {
	sort: {
		values: sortValues,
		defaultValue: sortValues[0],
		resetBehavior: ResetBehavior.ToDefault
	},
	stores: {
		resetBehavior: ResetBehavior.Clear
	},
	price: {
		values: priceValues,
		defaultValue: priceValues[0],
		resetBehavior: ResetBehavior.ToDefault
	}
}

export const gameOffersFilters = useFilters(gameOffersFiltersDefinition)

export const gameOffersFiltersOptions = useFiltersOptions(gameOffersFiltersDefinition, availableGameOffersFiltersOptions)