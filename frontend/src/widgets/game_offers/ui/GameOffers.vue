<script setup lang="ts">
import GameOfferCard from "./GameOfferCard.vue"
import LoadIndicator from "@/shared/ui/LoadIndicator.vue"
import type { Offer } from "@/entities/offer/model/Offer"
import { gameOffersFilters } from "@/features/game_info/filters/gameOffersFilters"
import { computed } from "vue"
import { useGameOffersFiltered } from "@/features/game_info/lib/useGameOffersFiltered"

const props = defineProps<{ offers: Offer[] }>()

const { filters } = gameOffersFilters

const gameOffersFiltered = computed(() => useGameOffersFiltered(props.offers, filters.value))
</script>

<template>
	<div class="game_offers">
		<template v-if="props.offers.length">
			<GameOfferCard  v-for="offer in gameOffersFiltered" 
			:key="offer.store_game_link"
			:offer="offer"/>
		</template>

		<LoadIndicator class="load_indicator" :is-short="false" v-else/>
	</div>
</template>

<style scoped>
.game_offers {
	--p_game_offers: 1rem;

	overflow: auto;
	padding: var(--p_game_offers);
	display: flex;
	flex-direction: column;
	align-items: center;
	width: 100%;
	gap: var(--p_game_offers);
	height: calc(4 * 5rem + 5 * var(--p_game_offers));
	border: 0.25rem solid var(--c_bg__surface);
	scrollbar-width: thin;
}

.load_indicator {
	margin: auto;
}
</style>