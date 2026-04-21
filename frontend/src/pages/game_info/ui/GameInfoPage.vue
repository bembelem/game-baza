<script lang="ts" setup>
import GameInfo from "@/widgets/game_info/ui/GameInfo.vue"
import type { GameBase } from "@/entities/game/model/Game";
import { useGameInfoStore } from "@/features/game_info/store/gameInfoStore"
import { useSearchGamesStore } from "@/features/search_games/store/searchGamesStore"
import { onMounted } from "vue"

const props = defineProps<{ gameID: GameBase["id"] }>()

const { gameInfo, updateGamePreview } = useGameInfoStore()
const { getGameByID } = useSearchGamesStore()

onMounted(() => {
	const newGamePreview = getGameByID(props.gameID)
	updateGamePreview(newGamePreview)
})
</script>

<template>
	<div class="game_info_page">
		<GameInfo :game-info="gameInfo"/>
	</div>
</template>

<style scoped>
.game_info_page {
	margin-top: var(--h_header);
	padding: 4rem;
	display: flex;
	flex-direction: column;
	flex: 1;
}

@media (max-width: 1024px) {
	.game_info_page {
		padding: 2rem;
	}
}
@media (max-width: 600px) {
	.game_info_page {
		padding: 1rem;
	}
}
</style>