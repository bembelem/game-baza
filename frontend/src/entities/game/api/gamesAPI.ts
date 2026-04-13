import type { GamesCatalog } from "../model/Game"


type SearchGamesParamsNames = 
	| "last_id"
	| "per_page"
	| "title"
	| "sort"
	| "genres"
	| "platforms"
	| "publishers"
	| "stores"
	| "price_min"
	| "price_max"

export type SearchGamesParams = Partial<Record<SearchGamesParamsNames, string[]>>


export const searchGamesFetch = async (
	searchGamesParams: SearchGamesParams, 
	abortController: AbortController
): Promise<GamesCatalog> => {
	const queryParams = new URLSearchParams()
	Object.entries(searchGamesParams).forEach(([paramName, paramValues]) => {
		paramValues?.forEach(value => queryParams.append(paramName, value))
	})

	const response = await fetch(`http://127.0.0.1:8000/games?${queryParams.toString()}`, { 
		method: "GET",
		signal: abortController.signal 
	}) 

	if (!response.ok) {
		throw new Error(`serachGamesError: ${response.status}`)
	}

	return await response.json()
}