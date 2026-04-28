<script setup lang="ts">
import GameOfferCard from "./GameOfferCard.vue"
import LoadIndicator from "@/shared/ui/LoadIndicator.vue"
import { mockOffers } from "@/entities/offer/data/mockOffers"
</script>

<template>
	<div class="game_offers">
		<template v-if="mockOffers">
			<GameOfferCard  v-for="offer in mockOffers" 
			:key="offer.store_game_link"
			:offer="offer" />
		</template>

		<LoadIndicator :is-short="false" v-else-if="!mockOffers"/>
		
		<p v-else>
			NO SIGNAL
		</p>
	</div>
</template>

<style scoped>
.game_offers {
	display: flex;
	flex-direction: column;
	width: 100%;
	gap: 1rem;
}
</style>