<script setup lang="ts">
import GameOfferCard from "./GameOfferCard.vue"
import LoadIndicator from "@/shared/ui/LoadIndicator.vue"
import type { Offer } from "@/entities/offer/model/Offer"
import { mockOffers } from "@/entities/offer/data/mockOffers"

const props = defineProps<{ offers: Offer[] }>()
</script>

<template>
	<div class="game_offers">
		<template v-if="props.offers.length">
			<GameOfferCard  v-for="offer in mockOffers" 
			:key="offer.store_game_link"
			:offer="offer"/>
		</template>

		<LoadIndicator :is-short="false" v-else/>
	</div>
</template>

<style scoped>
.game_offers {
	display: flex;
	flex-direction: column;
	align-items: center;
	width: 100%;
	gap: 1rem;
}
</style>