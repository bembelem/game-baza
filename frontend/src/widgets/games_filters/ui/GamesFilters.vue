<script setup lang="ts">
import { onMounted } from "vue"
import { useRoute } from "vue-router"
import MonoSelector from "@/shared/ui/MonoSelector.vue"
import MultiSelector from "@/shared/ui/MultiSelector.vue"
import { useSearchGamesStore } from "@/features/search_games/store/searchGamesStore"
import { searchGamesFilters, searchGamesFiltersOptions } from "@/features/search_games/filters/searchGamesFilters"
import { toSearchGamesParams } from "@/features/search_games/lib/gamesFiltersTransform"
import {
	genresFilterOptions,
	platformsFilterOptions,
	publishersFilterOptions,
	storesFilterOptions
} from "@/features/search_games/filters/searchGamesFiltersData"
import {
	getGenresFilterFetch,
	getPlatformsFilterFetch,
	getPublishersFilterFetch,
	getStoresFilterFetch
} from "@/entities/filter/api/filtersAPI"
import { fetchData } from "@/shared/lib/fetchData"

const route = useRoute()

const { gamesStore, searchGames, resetGames } = useSearchGamesStore()
const { filters, updateFilters, resetFilters } = searchGamesFilters
const { getFilterOptions } = searchGamesFiltersOptions

function onSubmit() {
	resetGames()
	const searchGamesParams = toSearchGamesParams(
		searchGamesFilters.filters.value,
		gamesStore.data.value?.last_id,
		gamesStore.data.value?.per_page
	)
	searchGames(searchGamesParams)
}

onMounted(() => {
	if (route.query.search) return

	fetchData(genresFilterOptions, getGenresFilterFetch)
	fetchData(platformsFilterOptions, getPlatformsFilterFetch)
	fetchData(publishersFilterOptions, getPublishersFilterFetch)
	fetchData(storesFilterOptions, getStoresFilterFetch)
})
</script>

<template>
	<div class="games_filters">
		<MonoSelector
		name="sort"
		:selected-option="filters.sort"
		:options="getFilterOptions('sort')"
		@option-click="updateFilters<'sort'>"/>

		<MultiSelector
		name="genres"
		:is-loading="genresFilterOptions.isPending.value"
		:selected-options="filters.genres"
		:options="getFilterOptions('genres')"
		label="жанры"
		@option-click="updateFilters<'genres'>"/>

		<MultiSelector
		name="platforms"
		:is-loading="platformsFilterOptions.isPending.value"
		:selected-options="filters.platforms"
		:options="getFilterOptions('platforms')"
		label="платформы"
		@option-click="updateFilters<'platforms'>"/>

		<MultiSelector
		name="publishers"
		:is-loading="publishersFilterOptions.isPending.value"
		:selected-options="filters.publishers"
		:options="getFilterOptions('publishers')"
		label="издатели"
		@option-click="updateFilters<'publishers'>"/>

		<MultiSelector
		name="stores"
		:is-loading="storesFilterOptions.isPending.value"
		:selected-options="filters.stores"
		:options="getFilterOptions('stores')"
		label="магазины"
		@option-click="updateFilters<'stores'>"/>

		<MonoSelector
		name="price"
		:selected-option="filters.price"
		:options="getFilterOptions('price')"
		@option-click="updateFilters<'price'>"/>

		<button
		class="button_reset"
		@click="resetFilters">
			Очистить
		</button>

		<button
		class="button_apply"
		@click="onSubmit">
			Применить
		</button>
	</div>
</template>

<style scoped>
.games_filters {
	display: grid;
	grid-template-columns: repeat(5, 1fr);
	gap: var(--space__xl);
}

.button_reset,
.button_apply {
	padding: var(--space__sm);
	font-size: var(--fs__lg);
	transition: color 0.1s ease-out
}

.button_reset {
	grid-column: 4;
	grid-row: 1;
	background-color: transparent;
	color: var(--c_brand__purple);
}
.button_reset:active {
  	color: var(--c_brand__purple_bright);
}

.button_apply {
	grid-column: 5;
	grid-row: 1;
	background-color: var(--c_brand__gold_bright);
}
.button_apply:active {
  	color: var(--c_text__primary);
}

@media (max-width: 1024px) {
	.games_filters {
		grid-template-columns: repeat(3, 1fr);
	}
	.button_reset {
		grid-column: 2;
	}
	.button_apply {
		grid-column: 3;
	}
}

@media (max-width: 600px) {
	.games_filters {
		grid-template-columns: repeat(2, 1fr);
	}
	.button_reset {
		grid-column: 1;
	}
	.button_apply {
		grid-column: 2;
	}
}
</style>