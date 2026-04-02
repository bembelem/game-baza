<script setup lang="ts">
import MonoSelector from "@/shared/ui/MonoSelector.vue"
import MultiSelector from "@/shared/ui/MultiSelector.vue"
import { searchGamesFilters, sortValues, priceValues } from "@/features/search_games/filters/searchGamesFilters"

const onValueClick = <K extends keyof typeof searchGamesFilters>(
	name: K, 
	value: typeof searchGamesFilters[K]
) => {
  	searchGamesFilters[name] = value
}
</script>

<template>
	<div class="games_filters">
		<MonoSelector
		name="sort"
		:value="searchGamesFilters.sort"
		:values="sortValues"
		@value-click="onValueClick<'sort'>"/>
		
		<MonoSelector
		name="price"
		:value="searchGamesFilters.price"
		:values="priceValues"
		@value-click="onValueClick<'price'>"/>

		<MultiSelector
		name="genres"
		:selected-values="searchGamesFilters.genres"
		:values="undefined"
		label="жанры"
		@value-click="onValueClick<'genres'>"/>

		<MultiSelector
		name="stores"
		:selected-values="searchGamesFilters.stores"
		:values="undefined"
		label="магазины"
		@value-click="onValueClick<'stores'>"/> 

		<button class="button_reset">Очистить</button>
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