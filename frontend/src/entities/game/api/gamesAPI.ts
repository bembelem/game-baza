import type { GamesCatalog, GameFull } from "../model/Game"
import type { Offer } from "@/entities/offer/model/Offer"
import { mockGameInfo } from "../data/mockGames"
import { mockOffers } from "@/entities/offer/data/mockOffers"


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


export interface GameInfoResponse extends GameFull {
	offers: Offer[]
}


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


const mockGameInfoResponse: GameInfoResponse = {
	...mockGameInfo,
	offers: [...mockOffers]
}


export const gameInfoFetch = async (
	gameID: string, 
	abortController: AbortController
): Promise<GameInfoResponse> => {
	const response = await fetch(`http://127.0.0.1:8000/games/${gameID}`, { 
		method: "GET",
		signal: abortController.signal 
	})
		
	if (!response.ok) {
		throw new Error(`gameInfoError: ${response.status}`)
	}

	return await response.json()	
}