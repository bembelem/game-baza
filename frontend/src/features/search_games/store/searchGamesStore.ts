import type { GamesCatalog } from "@/entities/game/model/Game"
import type { SearchGamesParams } from "@/entities/game/api/gamesAPI"
import { ref } from "vue"
import { useDataStore } from "@/shared/lib/useDataStore"
import { updateFetchDataController } from "@/shared/lib/fetchData"
import { searchGamesFetch } from "@/entities/game/api/gamesAPI"


const searchGamesController = ref<AbortController>()


export const searchGamesStore = {
	gamesStore: useDataStore<GamesCatalog>(),

	searchGames: async (searchGamesParams: SearchGamesParams) => {
		const newSearchGamesController = updateFetchDataController(searchGamesController)
		searchGamesStore.gamesStore.isPending.value = true

		try {
			const data = await searchGamesFetch(searchGamesParams, newSearchGamesController)

			if (!searchGamesStore.gamesStore.data.value) {
				searchGamesStore.gamesStore.data.value = data
			} else {
				data.items = [...searchGamesStore.gamesStore.data.value.items, ...data.items]
				searchGamesStore.gamesStore.data.value = data
			}
		} catch (error) {
			searchGamesStore.gamesStore.error.value = error instanceof Error 
				? error.message 
				: String(error)
		} finally {
			searchGamesController.value = undefined
			searchGamesStore.gamesStore.isPending.value = false
		}
	},

	resetGames: () => searchGamesStore.gamesStore.data.value = null
}