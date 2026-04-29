<script setup lang="ts">
import type { Offer } from "@/entities/offer/model/Offer"
import { type SearchGamesFilters, searchGamesFilters } from "@/features/search_games/filters/searchGamesFilters"
import { useRouter } from "vue-router"
import { searchGamesFiltersOptions } from "@/features/search_games/filters/searchGamesFilters"
import { Routes } from "@/shared/lib/router"

const router = useRouter()

const props = defineProps<{ offer: Offer }>()

const handleBuyClick = () => window.open(props.offer.store_game_link)

const { resetFilters, updateFilters } = searchGamesFilters
const { injectFilterOption } = searchGamesFiltersOptions

const handleMetadataClick = <K extends keyof SearchGamesFilters>(
	name: K,
	value: SearchGamesFilters[K]
) => {
	resetFilters()
	updateFilters(name, value)
	injectFilterOption(name, value)

	router.push({ name: Routes.games, query: { search: "true" } })
}
</script>

<template>
	<div class="game_offer_card">
		<button class="button_store" @click="() => handleMetadataClick('stores', [{ 
			title: props.offer.store, 
			value: props.offer.store 
		}])">
			{{ props.offer.store }}
		</button>

		<button class="button_price" @click="handleBuyClick">
			{{ props.offer.price_discount }}<span class="price--highlight">₽</span>
		</button>

		<button class="button_buy" @click="handleBuyClick">
			купить
		</button>
	</div>
</template>

<style scoped>
.game_offer_card {
	--fs_game_offer_card: 1.1rem;

	box-sizing: border-box;
	display: grid;
	justify-items: center;
	text-align: center;
	grid-template-columns: repeat(3, 1fr);
	grid-template-rows: 5rem;
	width: 100%;
	border: 0.25rem solid var(--c_bg__surface);
	background-color: var(--c_bg__surface);
	font-size: var(--fs_game_offer_card);
}

.button_store,
.button_buy {
	align-self: stretch;
	width: 100%;
	height: 100%;
	font-size: var(--fs_game_offer_card);
	cursor: pointer;
}

.button_store {
	overflow: hidden;
	white-space: nowrap;
	text-overflow: ellipsis;
	background-color: transparent;
	color: var(--c_secondary__accent);
}

.button_price {
	display: flex;
	width: 100%;
	height: 100%;
	justify-content: center;
	align-items: center;
	pointer-events: none;
	color: var(--c_text);
	background-color: var(--c_bg);
}
.price--highlight {
	margin-left: calc(var(--fs_game_offer_card) / 2);
}

.button_buy {
	background-color: var(--c_highlight__accent);
	transition: color 0.1s ease-out;
}

.button_buy:active,
.button_price:active {
	color: var(--c_text);
}

@media (max-width: 1024px) {
	.game_offer_card {
		grid-template-columns: repeat(2, 1fr);
	}
	.button_buy {
		display: none
	}
	.button_price {
		pointer-events: all;
		display: flex;
		justify-content: center;
		align-items: center;
		width: 100%;
		height: 100%;
		background-color: var(--c_highlight__accent);
		color: var(--c_bg);
		transition: color 0.1s ease-out;
		cursor: pointer;
	}
	.price--highlight {
		padding: 0;
	}
}
</style>