import { type SelectorValue, type FiltersDefinition, ResetBehavior } from "@/shared/interface/Filters"
import { sortValues, availableSearchGamesFiltersOptions } from "./searchGamesFiltersData"
import { priceValues } from "@/shared/data/filtersValues"
import { useFilters } from "@/shared/lib/useFilters"
import { useFiltersOptions } from "@/shared/lib/useFiltersOptions"


export interface SearchGamesFilters {
 	sort: SelectorValue<string>,
	genres: SelectorValue<string>[],
	platforms: SelectorValue<string>[],
	developers: SelectorValue<string>[]
	publishers: SelectorValue<string>[],
	stores: SelectorValue<string>[],
	price: SelectorValue<[number, number | undefined] | undefined>
}

type SearchGamesFiltersDefinition = FiltersDefinition<SearchGamesFilters>


export const searchGamesFiltersDefinition: SearchGamesFiltersDefinition = {
	sort: {
		values: sortValues,
		defaultValue: sortValues[0],
		resetBehavior: ResetBehavior.ToDefault
	},
	genres: {
		resetBehavior: ResetBehavior.Clear
	},
	platforms: {
		resetBehavior: ResetBehavior.Clear 
	},
	developers: {
		resetBehavior: ResetBehavior.Clear
	},
	publishers: {
		resetBehavior: ResetBehavior.Clear
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

export const searchGamesFilters = useFilters(searchGamesFiltersDefinition)

export const searchGamesFiltersOptions = useFiltersOptions(searchGamesFiltersDefinition, availableSearchGamesFiltersOptions)