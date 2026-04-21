import { type GameInfoResponse, gameInfoFetch } from "@/entities/game/api/gamesAPI"
import type { GameBase, GameFull } from "@/entities/game/model/Game"
import { ref, computed } from "vue"
import { useDataStore } from "@/shared/lib/useDataStore"
import { fetchData, updateFetchDataController } from "@/shared/lib/fetchData"


const gameInfoController = ref<AbortController>() 
const gamePreview = ref<GameBase>()
const gameInfoStore = useDataStore<GameInfoResponse>()


export const useGameInfoStore = () => {
	const gameBaseInfo = computed(() => gamePreview.value ?? gameInfoStore.data.value)

	const gameInfo = computed((): Partial<GameFull> => { 
		const { offers, ...gameFullInfo } = gameInfoStore.data.value ?? {} 

		return {
			...gameBaseInfo.value,
			...gameFullInfo,
		}
	})

	async function fetchGameInfo(gameID: GameBase["id"]) {
		const newGameInfoController = updateFetchDataController(gameInfoController)
		gameInfoStore.data.value = null

		await fetchData(gameInfoStore, () => gameInfoFetch(gameID, newGameInfoController))
		gameInfoController.value = undefined
	}

	function updateGamePreview(newGamePreview?: GameBase) {
		if (!newGamePreview) return

		if (newGamePreview.id === gamePreview.value?.id) return

		gamePreview.value = newGamePreview

		fetchGameInfo(newGamePreview.id)
	}
	
	return {
		gameInfo,
		fetchGameInfo,
		updateGamePreview
	}
}