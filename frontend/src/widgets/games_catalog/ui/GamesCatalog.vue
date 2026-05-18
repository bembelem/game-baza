<script setup lang="ts">
import { onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import GameCard from "./GameCard.vue"
import LoadIndicator from "@/shared/ui/LoadIndicator.vue"
import type { GameBase } from "@/entities/game/model/Game"
import { useSearchGamesStore } from "@/features/search_games/store/searchGamesStore"
import { toSearchGamesParams } from "@/features/search_games/lib/gamesFiltersTransform"
import { searchGamesFilters } from "@/features/search_games/filters/searchGamesFilters"
import { Routes } from "@/shared/lib/router"

const route = useRoute()
const router = useRouter()

const { gamesStore, searchGames, resetGames } = useSearchGamesStore()

function handleGameCardClick(gameID: GameBase["id"]) {
 	router.push({ name: Routes.gameInfo, params: { gameID } })
}

function handleSearch() {
	const searchGamesParams = toSearchGamesParams(
		searchGamesFilters.filters.value,
		gamesStore.data.value?.last_id,
		gamesStore.data.value?.per_page
	)
	searchGames(searchGamesParams)
}

onMounted(() => {
	if (route.query.search) {
		resetGames()
		router.replace({ name: Routes.games })
	}
	handleSearch()
})
</script>

<template>
  	<div class="games_gallery">
		<GameCard
		v-for="game in gamesStore.data.value?.items"
		:key="game.id"
		:game="game"
		@click="() => handleGameCardClick(game.id)"/>

		<div class="load_container">
			<div
			v-if="gamesStore.isPending.value"
			class="load_indicator">
				<LoadIndicator :is-short="false"/>
			</div>

			<button
			v-else-if="gamesStore.data.value?.has_more"
			class="load_button"
			@click="handleSearch">
				хочу ещё!
			</button>

			<p
			v-else
			class="load_message--over">
				GAMES OVER
			</p>
		</div>
	</div>
</template>

<style scoped>
.games_gallery {
	display: grid;
	grid-template-columns: repeat(3, 1fr);
	gap: var(--space__xl);
}

.load_container {
	--fs_load: var(--fs__2xl);

	display: flex;
	justify-content: center;
	grid-column: 1 / -1;
	font-size: var(--fs__2xl);
}

.load_indicator,
.load_button {
  	padding: var(--space__md) var(--space__xl);
}
.load_button {
	background-color: var(--c_brand__gold_bright);
}

.load_message--over {
	color: var(--c_text__muted);
	text-decoration: underline;
	user-select: none;
}

@media (max-width: 1024px) {
	.games_gallery {
		grid-template-columns: repeat(2, 1fr);
	}
}

@media (max-width: 600px) {
	.games_gallery {
		grid-template-columns: 1fr;
	}
	.load_button {
		width: 100%;
	}
}
</style>