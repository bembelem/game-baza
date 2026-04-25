import type { SelectorValue } from "@/shared/interface/Filters"
import { useDataStore } from "@/shared/lib/useDataStore"
import { fetchData } from "@/shared/lib/fetchData"
import { getGenresFilterFetch } from "@/entities/filter/api/filtersAPI"
import { getPlatformsFilterFetch } from "@/entities/filter/api/filtersAPI"
import { getPublishersFilterFetch } from "@/entities/filter/api/filtersAPI"
import { getStoresFilterFetch } from "@/entities/filter/api/filtersAPI"


export const genresFilterOptions = useDataStore<SelectorValue<string>[]>()
export const platformsFilterOptions = useDataStore<SelectorValue<string>[]>()
export const publishersFilterOptions = useDataStore<SelectorValue<string>[]>()
export const storesFilterOptions = useDataStore<SelectorValue<string>[]>()


export function searchGamesFiltersFetch() {
	fetchData(genresFilterOptions, getGenresFilterFetch)
	fetchData(platformsFilterOptions, getPlatformsFilterFetch)
	fetchData(publishersFilterOptions, getPublishersFilterFetch)
	fetchData(storesFilterOptions, getStoresFilterFetch)
}