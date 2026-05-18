<script lang="ts" setup>
import { useTemplateRef, provide, onMounted } from "vue"
import GameInfo from "@/widgets/game_info/ui/GameInfo.vue"
import GameOffersFilters from "@/widgets/game_offers_filters/ui/GameOffersFilters.vue"
import GameOffers from "@/widgets/game_offers/ui/GameOffers.vue"
import type { GameBase } from "@/entities/game/model/Game"
import { useGameInfoStore } from "@/features/game_info/store/gameInfoStore"
import { useSearchGamesStore } from "@/features/search_games/store/searchGamesStore"

const props = defineProps<{ gameID: GameBase["id"] }>()

const { gameInfo, gameOffers, updateGamePreview } = useGameInfoStore()
const { getGameByID } = useSearchGamesStore()

const gameOffersTemplateRef = useTemplateRef("gameOffers")

function handleScrollToGameOffers() {
	if (!gameOffersTemplateRef.value) return

	gameOffersTemplateRef.value.scrollIntoView({
		behavior: "smooth",
		block: "nearest",
	})
}

provide("scrollToGameOffers", handleScrollToGameOffers)

onMounted(() => {
	const newGamePreview = getGameByID(props.gameID)
	updateGamePreview(props.gameID, newGamePreview)
})
</script>

<template>
	<div class="game_info_page">
		<GameInfo
		:game-info="gameInfo"
		@scroll-to-game-offers="handleScrollToGameOffers"/>

		<section
		ref="gameOffers"
		class="game_offers_section">
			<h2 class="game_offers_title">
				ПРЕДЛОЖЕНИЯ
			</h2>
			<GameOffersFilters/>
			<GameOffers :offers="gameOffers"/>
		</section>
	</div>
</template>

<style scoped>
.game_info_page {
	display: flex;
	flex-direction: column;
	gap: var(--space__2xl);
}

.game_offers_section {
	display: flex;
	flex-direction: column;
	gap: var(--space__md);
}

.game_offers_title {
	font-size: var(--fs__2xl);
	color: var(--c_text__primary);
}
</style>