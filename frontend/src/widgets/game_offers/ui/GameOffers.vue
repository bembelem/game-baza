<script setup lang="ts">
import { computed } from "vue"
import GameOfferCard from "./GameOfferCard.vue"
import LoadIndicator from "@/shared/ui/LoadIndicator.vue"
import type { Offer } from "@/entities/offer/model/Offer"
import { gameOffersFilters } from "@/features/game_info/filters/gameOffersFilters"
import { useGameOffersFiltered } from "@/features/game_info/lib/useGameOffersFiltered"

const props = defineProps<{ offers: Offer[] }>()

const { filters } = gameOffersFilters

const gameOffersFiltered = computed(() => useGameOffersFiltered(props.offers, filters.value))
</script>

<template>
	<div class="game_offers">
		<template v-if="props.offers.length">
			<GameOfferCard
			v-for="offer in gameOffersFiltered"
			:key="offer.store_game_link"
			:offer="offer"/>
		</template>

		<LoadIndicator
		v-else
		class="load_indicator"
		:is-short="false"/>
	</div>
</template>

<style scoped>
.game_offers {
	--h_card: 5rem;
	--p_game_offers: var(--space__lg);

	display: flex;
	flex-direction: column;
	overflow: auto;
	height: calc(var(--h_card) * 4 + 5 * var(--p_game_offers) + var(--border__md) * 2);
	padding: var(--p_game_offers);
	gap: var(--p_game_offers);
	border: var(--border__md) solid var(--c_bg__surface);
	scrollbar-width: thin;
}

.load_indicator {
	--fs_load: var(--fs__2xl);

	margin: auto;
}

@media (max-width: 1024px) {
	.game_offers {
		height: auto;
	}
}
</style>