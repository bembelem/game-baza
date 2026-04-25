import type { AvailableFiltersOptions, InjectedFiltersOptions } from "@/shared/interface/Filters"
import type { ToArray } from "@/shared/interface/Helpers"
import { genresFilterOptions } from "./searchGamesFiltersData"
import { publishersFilterOptions } from "./searchGamesFiltersData"
import { reactive } from "vue"
import { type SearchGamesFilters, searchGamesFiltersDefinition } from "./searchGamesFilters"


const availableFiltersOptions: AvailableFiltersOptions<SearchGamesFilters> = {
	genres: genresFilterOptions.data,
	publishers: publishersFilterOptions.data
}

const injectedFiltersOptions = reactive<InjectedFiltersOptions<SearchGamesFilters>>({})


export function getSearchGamesFilterOptions<K extends keyof SearchGamesFilters>(name: K) {
	if (searchGamesFiltersDefinition[name].values) {
		return searchGamesFiltersDefinition[name].values as ToArray<SearchGamesFilters[K]>
	}

	const availableOptions = availableFiltersOptions[name]?.value ?? []
	const injectedOptions = injectedFiltersOptions[name] ?? []

	const combined = [...availableOptions, ...injectedOptions]

	return combined.filter((item, index) => 
		[...availableOptions, ...injectedOptions].findIndex((i) => i.value === item.value) === index
	) as ToArray<SearchGamesFilters[K]>
}


export function injectSearchGamesFilterOption<K extends keyof SearchGamesFilters>(
	name: K,
	value: SearchGamesFilters[K]
) {
	if (!injectedFiltersOptions[name]) {
		injectedFiltersOptions[name] = []
	}
	
	if (Array.isArray(value)) {
    	value.forEach((item) => {
			// known TS limitation with generic index access
			// eslint-disable-next-line @typescript-eslint/no-explicit-any
			injectedFiltersOptions[name]!.push(item as any)
		})
	} else {
		// eslint-disable-next-line @typescript-eslint/no-explicit-any
		injectedFiltersOptions[name]!.push(value as any)
	}
}