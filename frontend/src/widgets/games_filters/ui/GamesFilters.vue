<script setup lang="ts">
import MonoSelector from "@/shared/ui/MonoSelector.vue"
import MultiSelector from "@/shared/ui/MultiSelector.vue"
import { useRoute } from "vue-router"
import { useSearchGamesStore } from "@/features/search_games/store/searchGamesStore"
import { searchGamesFilters, searchGamesFiltersOptions } from "@/features/search_games/filters/searchGamesFilters"
import { toSearchGamesParams } from "@/features/search_games/lib/gamesFiltersTransform"
import { onMounted } from "vue"
import { fetchData } from "@/shared/lib/fetchData"
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

const route = useRoute()

const { searchGames, resetGames } = useSearchGamesStore()
const { filters, updateFilters, resetFilters } = searchGamesFilters
const { getFilterOptions } = searchGamesFiltersOptions

onMounted(() => {
	if (route.query.search) return

	fetchData(genresFilterOptions, getGenresFilterFetch)
	fetchData(platformsFilterOptions, getPlatformsFilterFetch)
	fetchData(publishersFilterOptions, getPublishersFilterFetch)
	fetchData(storesFilterOptions, getStoresFilterFetch)
})

const onSubmit = (() => {
	resetGames()
	const searchGamesParams = toSearchGamesParams(filters.value)
	searchGames(searchGamesParams)
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
		:selected-options="filters.genres"
		:options="getFilterOptions('genres')"
		:is-loading="genresFilterOptions.isPending.value"
		label="жанры"
		@option-click="updateFilters<'genres'>"/>

		<MultiSelector
		name="platforms"
		:selected-options="filters.platforms"
		:options="getFilterOptions('platforms')"
		:is-loading="platformsFilterOptions.isPending.value"
		label="платформы"
		@option-click="updateFilters<'platforms'>"/>

		<MultiSelector
		name="publishers"
		:selected-options="filters.publishers"
		:options="getFilterOptions('publishers')"
		:is-loading="publishersFilterOptions.isPending.value"
		label="издатели"
		@option-click="updateFilters<'publishers'>"/>

		<MultiSelector
		name="stores"
		:selected-options="filters.stores"
		:options="getFilterOptions('stores')"
		:is-loading="storesFilterOptions.isPending.value"
		label="магазины"
		@option-click="updateFilters<'stores'>"/>

		<MonoSelector
		name="price"
		:selected-option="filters.price"
		:options="getFilterOptions('price')"
		@option-click="updateFilters<'price'>"/>

		<button class="button_reset" @click="resetFilters">Очистить</button>
		<button class="button_apply" @click="onSubmit">Применить</button>
	</div>
</template>

<style scoped>
.games_filters {
	padding: 1.5rem 0 4rem;
	display: grid;
	grid-template-columns: repeat(5, 1fr);
	gap: 2rem;
	width: 100%;
}

.button_reset,
.button_apply {
	padding: 0.5rem;
	font-size: 1.2rem;
	transition: color 0.1s ease-out, 
				transform 0.1s ease-out;
}

.button_reset {
	grid-column: 4;
	grid-row: 1;
	background-color: transparent;
	color: var(--c_secondary);
}
.button_reset:active {
	color: var(--c_secondary__accent);
}

.button_apply {
	grid-column: 5;
	grid-row: 1;
	background-color: var(--c_highlight__accent);
}
.button_apply:active {
	color: var(--c_text);
}

@media (max-width: 1024px) {
	.games_filters {
		grid-template-columns: repeat(3, 1fr);
		gap: 1rem;
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
		gap: 0.5rem;
	}
	.button_apply,
	.button_reset {
		font-size: 1rem;
	}
	.button_reset {
		grid-column: 1;
	}
	.button_apply {
		grid-column: 2;
	}
}
</style>