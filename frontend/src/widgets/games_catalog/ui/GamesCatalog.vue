<script setup lang="ts">
import GameCard from "./GameCard.vue"
import LoadIndicator from "@/shared/ui/LoadIndicator.vue"
import type { GameBase } from "@/entities/game/model/Game"
import { useRouter } from "vue-router"
import { useSearchGamesStore } from "@/features/search_games/store/searchGamesStore"
import { Routes } from "@/shared/lib/router"
import { toSearchGamesParams } from "@/features/search_games/lib/gamesFiltersTransform"
import { searchGamesFilters } from "@/features/search_games/filters/searchGamesFilters"
import { onMounted } from "vue"

const router = useRouter()

const { gamesStore, searchGames } = useSearchGamesStore()

const handleGameCardClick = (gameID: GameBase["id"]) => {
	router.push({ name: Routes.gameInfo, params: { gameID: gameID } })
}

const onSubmit = () => {
	const searchGamesParams = toSearchGamesParams(searchGamesFilters.filters.value)
	searchGames(searchGamesParams)
}

onMounted(() => onSubmit())
</script>

<template>
	<div class="games_gallary">
		<GameCard v-for="game in gamesStore.data.value?.items"
		:key="game.id"
		:game="game"
		@click="() => handleGameCardClick(game.id)"/>
		
		<div class="load_container">
			<div class="load_indicator" v-if="gamesStore.isPending.value">
				<LoadIndicator :is-short="false"/>
			</div>
			
			<button class="load_button" 
			@click="onSubmit"
			v-else-if="gamesStore.data.value?.has_more">
				хочу ещё!
			</button>

			<p class="load_message--over" v-else>
				GAMES OVER
			</p>
		</div>
	</div>
</template>

<style scoped>
.games_gallary {
	--fs_load: 2rem;

	display: grid;
	grid-template-columns: repeat(3, 1fr);
	gap: 2rem;
	width: 100%;
}

.load_container {
	display: flex;
	justify-content: center;
	grid-column: 1 / -1;
	grid-row: auto;
	width: 100%;
	height: auto;
}

.load_indicator,
.load_button {
	padding: calc(var(--fs_load) / 2) var(--fs_load);
}

.load_button {
	background-color: var(--c_highlight__accent);
	font-size: var(--fs_load);
}

.load_message--over {
	font-size: var(--fs_load);
	text-decoration: underline;
	color: var(--c_placeholder);
	user-select: none;
}
@media (max-width: 1024px) {
	.games_gallary {
		gap: 1rem;
		grid-template-columns: repeat(2, 1fr);
	}
}
@media (max-width: 600px) {
	.games_gallary {
		grid-template-columns: 1fr;
		gap: 0.5rem;
	}
	.load_container {
		--fs_load: 1.5rem;
	}
	.load_button {
		width: 100%;
	}
}
</style>