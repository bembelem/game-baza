<script setup lang="ts">
import { useRouter } from "vue-router"
import { Routes } from "@/shared/lib/router"
import type { Offer } from "@/entities/offer/model/Offer"
import { type SearchGamesFilters, searchGamesFilters, searchGamesFiltersOptions } from "@/features/search_games/filters/searchGamesFilters"

const props = defineProps<{ offer: Offer }>()

const router = useRouter()

const { resetFilters, updateFilters } = searchGamesFilters
const { injectFilterOption } = searchGamesFiltersOptions

function handleBuyClick() {
	window.open(props.offer.store_game_link)
}

function handleMetadataClick<K extends keyof SearchGamesFilters>(
	name: K,
	value: SearchGamesFilters[K]
) {
	resetFilters()
	updateFilters(name, value)
	injectFilterOption(name, value)

	router.push({ name: Routes.games, query: { search: "true" } })
}
</script>

<template>
	<div class="game_offer_card">
		<button
		class="button_store"
		@click="() => handleMetadataClick('stores', [{
			title: props.offer.store,
			value: props.offer.store,
		}])">
			{{ props.offer.store }}
		</button>

		<button
		class="button_price"
		@click="handleBuyClick">
			{{ props.offer.price_discount }}<span class="price--highlight">₽</span>
		</button>

		<button
		class="button_buy"
		@click="handleBuyClick">
			купить
		</button>
	</div>
</template>

<style scoped>
.game_offer_card {
	--fs_game_offer_card: var(--fs__sm);

	display: grid;
	grid-template-columns: repeat(3, 1fr);
	justify-items: center;
	flex-shrink: 0;
	width: 100%;
	height: var(--h_card);
	border: var(--border__sm) solid var(--c_bg__surface);
	background-color: var(--c_bg__surface);
	font-size: var(--fs_game_offer_card);
	text-align: center;
}

.button_store,
.button_buy {
	width: 100%;
	font-size: var(--fs_game_offer_card);
	cursor: pointer;
}

.button_store {
	overflow: hidden;
	background-color: transparent;
	color: var(--c_brand__purple_bright);
	white-space: nowrap;
	text-overflow: ellipsis;
}

.button_price {
	display: flex;
	justify-content: center;
	align-items: center;
	width: 100%;
	background-color: var(--c_bg__primary);
	color: var(--c_text__primary);
	pointer-events: none;
}

.price--highlight {
	margin-left: calc(var(--fs_game_offer_card) / 2);
}

.button_buy {
	background-color: var(--c_brand__gold_bright);
	transition: color 0.1s ease-out;
}

.button_buy:active,
.button_price:active {
	color: var(--c_text__primary);
}

@media (max-width: 1024px) {
	.game_offer_card {
		grid-template-columns: repeat(2, 1fr);
	}
	.button_buy {
		display: none;
	}
	.button_price {
		background-color: var(--c_brand__gold_bright);
		color: var(--c_bg__primary);
		cursor: pointer;
		pointer-events: all;
		transition: color 0.1s ease-out;
	}
	.price--highlight {
		padding: 0;
	}
}
</style>