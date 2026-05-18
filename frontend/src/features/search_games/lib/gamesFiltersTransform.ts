import type { SearchGamesFilters } from "@/features/search_games/filters/searchGamesFilters"
import type { SearchGamesParams } from "@/entities/game/api/gamesAPI"
import type { GamesCatalog } from "@/entities/game/model/Game"


export function toSearchGamesParams(
	searchGamesFilters: Partial<SearchGamesFilters>,
	lastID: GamesCatalog["last_id"] | undefined,
	perPage: GamesCatalog["per_page"] | undefined
): SearchGamesParams {
	const  { sort, price, ...filters } = searchGamesFilters

	return {
		last_id: lastID ? [String(lastID)] : undefined,
		per_page: perPage ? [String(perPage)] : undefined,
		sort: sort?.value ? [sort.value] : undefined,
	 	genres: filters.genres?.map(value => value.value),
	 	platforms: filters.platforms?.map(value => value.value),
	 	publishers: filters.publishers?.map(value => value.value),
	 	stores: filters.stores?.map(value => value.value),
	 	price_min: price?.value?.[0] != undefined ? [String(price.value?.[0])] : undefined,
	 	price_max: price?.value?.[1] != undefined ? [String(price.value?.[1])] : undefined
	}
}