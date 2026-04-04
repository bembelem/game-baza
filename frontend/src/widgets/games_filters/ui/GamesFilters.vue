<script setup lang="ts">
import MonoSelector from "@/shared/ui/MonoSelector.vue"
import MultiSelector from "@/shared/ui/MultiSelector.vue"
import type { SearchGamesFilters } from "@/features/search_games/filters/searchGamesFilters"
import { sortValues, priceValues, searchGamesFiltersDefinition } from "@/features/search_games/filters/searchGamesFilters"
import { useFilters } from "@/shared/lib/useFilters"

const { filters, updateFilters, resetFilters } = useFilters<SearchGamesFilters>(searchGamesFiltersDefinition)
</script>

<template>
	<div class="games_filters">
		<MonoSelector
		name="sort"
		:value="filters.sort"
		:values="sortValues"
		@value-click="updateFilters<'sort'>"/>
		
		<MonoSelector
		name="price"
		:value="filters.price"
		:values="priceValues"
		@value-click="updateFilters<'price'>"/>

		<MultiSelector
		name="genres"
		:selected-values="filters.genres"
		:values="undefined"
		label="жанры"
		@value-click="updateFilters<'genres'>"/>

		<MultiSelector
		name="stores"
		:selected-values="filters.stores"
		:values="undefined"
		label="магазины"
		@value-click="updateFilters<'stores'>"/> 

		<button class="button_reset" @click="resetFilters">Очистить</button>
		<button class="button_apply">Применить</button>
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