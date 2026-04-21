import type { GamesCatalog } from "@/entities/game/model/Game"
import type { SearchGamesParams } from "@/entities/game/api/gamesAPI"
import { ref } from "vue"
import { useDataStore } from "@/shared/lib/useDataStore"
import { updateFetchDataController } from "@/shared/lib/fetchData"
import { searchGamesFetch } from "@/entities/game/api/gamesAPI"


const searchGamesController = ref<AbortController>()
const gamesStore = useDataStore<GamesCatalog>()


export const useSearchGamesStore = () => {
	async function searchGames(searchGamesParams: SearchGamesParams) {
		const newSearchGamesController = updateFetchDataController(searchGamesController)
		gamesStore.isPending.value = true

		try {
			const data = await searchGamesFetch(searchGamesParams, newSearchGamesController)

			if (!gamesStore.data.value) {
				gamesStore.data.value = data
			} else {
				data.items = [...gamesStore.data.value.items, ...data.items]
				gamesStore.data.value = data
			}
		} catch (error) {
			gamesStore.error.value = error instanceof Error 
				? error.message 
				: String(error)
		} finally {
			searchGamesController.value = undefined
			gamesStore.isPending.value = false
		}
	}

	function getGameByID(gameID: string) {
		return gamesStore.data.value?.items.find((game) => game.id == gameID)
	} 

	function resetGames() {
		gamesStore.data.value = null
	}

	return {
		gamesStore,
		searchGames,
		getGameByID,
		resetGames
	}
}