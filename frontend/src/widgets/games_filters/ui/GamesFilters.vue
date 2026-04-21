<script setup lang="ts">
import MonoSelector from "@/shared/ui/MonoSelector.vue"
import MultiSelector from "@/shared/ui/MultiSelector.vue"
import type { SelectorValue } from "@/shared/interface/Filters"
import { searchGamesFilters } from "@/features/search_games/filters/searchGamesFilters"
import { searchGamesFiltersDefinition } from "@/features/search_games/filters/searchGamesFilters"
import { useDataStore } from "@/shared/lib/useDataStore"
import { fetchData } from "@/shared/lib/fetchData"
import { getGenresFilterFetch, getPlatformsFilterFetch, getPublishersFilterFetch, getStoresFilterFetch } from "@/entities/filter/api/filtersAPI"
import { onMounted } from "vue"
import { useSearchGamesStore } from "@/features/search_games/store/searchGamesStore"
import { toSearchGamesParams } from "@/features/search_games/lib/gamesFiltersTransform"

const { searchGames, resetGames } = useSearchGamesStore()
const { filters, updateFilters, resetFilters } = searchGamesFilters

const genresFilterValues = useDataStore<SelectorValue<string>[]>()
const platformsFilterValues = useDataStore<SelectorValue<string>[]>()
const publishersFilterValues = useDataStore<SelectorValue<string>[]>()
const storesFilterValues = useDataStore<SelectorValue<string>[]>()

onMounted(() => {
	fetchData(genresFilterValues, getGenresFilterFetch)
	fetchData(platformsFilterValues, getPlatformsFilterFetch)
	fetchData(publishersFilterValues, getPublishersFilterFetch)
	fetchData(storesFilterValues, getStoresFilterFetch)
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
		:value="filters.sort"
		:values="searchGamesFiltersDefinition.sort.values"
		@value-click="updateFilters<'sort'>"/>

		<MultiSelector
		name="genres"
		:selected-values="filters.genres"
		:values="genresFilterValues.data.value"
		label="жанры"
		@value-click="updateFilters<'genres'>"/>

		<MultiSelector
		name="platforms"
		:selected-values="filters.platforms"
		:values="platformsFilterValues.data.value"
		label="платформы"
		@value-click="updateFilters<'platforms'>"/>

		<MultiSelector
		name="publishers"
		:selected-values="filters.publishers"
		:values="publishersFilterValues.data.value"
		label="издатели"
		@value-click="updateFilters<'publishers'>"/>

		<MultiSelector
		name="stores"
		:selected-values="filters.stores"
		:values="storesFilterValues.data.value"
		label="магазины"
		@value-click="updateFilters<'stores'>"/>

		<MonoSelector
		name="price"
		:value="filters.price"
		:values="searchGamesFiltersDefinition.price.values"
		@value-click="updateFilters<'price'>"/>

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