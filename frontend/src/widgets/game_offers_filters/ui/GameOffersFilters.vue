<script setup lang="ts">
import MonoSelector from "@/shared/ui/MonoSelector.vue"
import MultiSelector from "@/shared/ui/MultiSelector.vue"
import { gameOffersFilters } from "@/features/game_info/filters/gameOffersFilters"
import { gameOffersFiltersOptions } from "@/features/game_info/filters/gameOffersFilters"

const { filters, updateFilters, resetFilters } = gameOffersFilters

const { getFilterOptions } = gameOffersFiltersOptions
</script>

<template>
	<div class="games_filters">
		<MonoSelector
		name="sort"
		:selected-option="filters.sort"
		:options="getFilterOptions('sort')"
		@option-click="updateFilters<'sort'>"/>

		<MultiSelector
		name="stores"
		:selected-options="filters.stores"
		:options="getFilterOptions('stores')"
		:is-loading="Boolean(!getFilterOptions('stores').length)"
		label="магазины"
		@option-click="updateFilters<'stores'>"/>

		<MonoSelector
		name="price"
		:selected-option="filters.price"
		:options="getFilterOptions('price')"
		@option-click="updateFilters<'price'>"/>

		<button class="button_reset" @click="resetFilters">Очистить</button>
	</div>
</template>

<style scoped>
.games_filters {
	padding: 1.5rem 0 4rem;
	display: grid;
	grid-template-columns: repeat(4, 1fr);
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