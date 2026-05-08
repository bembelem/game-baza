<script setup lang="ts">
import MonoSelector from "@/shared/ui/MonoSelector.vue"
import MultiSelector from "@/shared/ui/MultiSelector.vue"
import { gameOffersFilters, gameOffersFiltersOptions } from "@/features/game_info/filters/gameOffersFilters"

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

		<button
		class="button_reset"
		@click="resetFilters">
			Очистить
		</button>
	</div>
</template>

<style scoped>
.games_filters {
	display: grid;
	grid-template-columns: repeat(4, 1fr);
	gap: var(--space__xl);
}

.button_reset {
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

@media (max-width: 1024px) {
	.games_filters {
		grid-template-columns: repeat(3, 1fr);
	}
	.button_reset {
		grid-column: 2;
	}
}

@media (max-width: 600px) {
	.games_filters {
		grid-template-columns: repeat(2, 1fr);
	}
	.button_reset {
		grid-column: 1;
	}
}
</style>