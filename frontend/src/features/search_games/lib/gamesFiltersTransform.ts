import type { SearchGamesFilters } from "@/features/search_games/filters/searchGamesFilters"
import type { SearchGamesParams } from "@/entities/game/api/gamesAPI"


export function toSearchGamesParams(searchGamesFilters: Partial<SearchGamesFilters>): SearchGamesParams {
	const  { sort, price, ...filters } = searchGamesFilters

	return {
		sort: sort?.value ? [sort.value] : undefined,
	 	genres: filters.genres?.map(value => value.value),
	 	platforms: filters.platforms?.map(value => value.value),
	 	publishers: filters.publishers?.map(value => value.value),
	 	stores: filters.stores?.map(value => value.value),
	 	price_min: price?.value?.[0] != undefined ? [String(price.value?.[0])] : undefined,
	 	price_max: price?.value?.[1] != undefined ? [String(price.value?.[1])] : undefined
	}
}