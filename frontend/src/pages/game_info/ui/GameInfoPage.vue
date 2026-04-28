<script lang="ts" setup>
import GameInfo from "@/widgets/game_info/ui/GameInfo.vue"
import GameOffers from "@/widgets/game_offers/ui/GameOffers.vue"
import type { GameBase } from "@/entities/game/model/Game"
import { useGameInfoStore } from "@/features/game_info/store/gameInfoStore"
import { useSearchGamesStore } from "@/features/search_games/store/searchGamesStore"
import { onMounted } from "vue"

const props = defineProps<{ gameID: GameBase["id"] }>()

const { gameInfo, gameOffers, updateGamePreview } = useGameInfoStore()
const { getGameByID } = useSearchGamesStore()

onMounted(() => {
	const newGamePreview = getGameByID(props.gameID)
	updateGamePreview(props.gameID, newGamePreview)
})
</script>

<template>
	<div class="game_info_page">
		<GameInfo :game-info="gameInfo"/>

		<section class="game_offers_section">
			<h2 class="game_offers_title">
				ПРЕДЛОЖЕНИЯ
			</h2>

			<GameOffers :offers="gameOffers"/>
		</section>
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

.game_offers_section {
	display: flex;
	flex-direction: column;
	padding: 1.5rem 0;
	gap: 1.5rem;
}

.game_offers_title {
	font-size: 2rem;
	color: var(--c_highlight__accent);
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