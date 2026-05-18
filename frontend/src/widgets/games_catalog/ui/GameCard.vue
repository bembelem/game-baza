<script setup lang="ts">
import type { GameBase } from "@/entities/game/model/Game"

const props = defineProps<{
	game: GameBase,
	onClick: () => void
}>()
</script>

<template>
	<div
	class="game_card"
	@click="props.onClick">
		<img
		class="game_image"
		alt="обложка игры"
		:src="props.game.image_url"/>

		<div class="info_container">
			<p class="title">{{ props.game.title }}</p>
			<p v-if="props.game.min_price_discount == 0">бесплатно</p>
			<p v-else>
				от
				<span class="min_price--highlighted">{{ props.game.min_price_discount }}₽</span>
			</p>
		</div>
	</div>
</template>

<style scoped>
.game_card {
	display: flex;
	flex-direction: column;
	overflow: hidden;
	background-color: var(--c_bg__surface);
	box-shadow:
		0 0.5rem 1.5rem rgba(0, 0, 0, 0.4),
		0 0.125rem 0.375rem rgba(0, 0, 0, 0.3);
	cursor: pointer;
}

.game_image {
	width: 100%;
	aspect-ratio: 2.14 / 1;
	object-fit: cover;
	object-position: center;
}

.info_container {
	display: flex;
	flex-direction: column;
	justify-content: space-between;
	height: 100%;
	padding: var(--space__sm);
	gap: var(--space__xs);
	font-size: var(--fs__xs);
}

.title {
	display: -webkit-box;
	overflow: hidden;
	-webkit-box-orient: vertical;
	-webkit-line-clamp: 2;
	text-overflow: ellipsis;
}

.min_price--highlighted {
  	font-size: var(--fs__md);
}
</style>