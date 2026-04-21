<script setup lang="ts">
import type { GameBase } from "@/entities/game/model/Game"

const { game } = defineProps<{ 
	game: GameBase,
	onClick: () => void
}>()
</script>

<template>
	<div class="game_card" @click="$props.onClick">
		<img 
		class="game_image"
		alt="обложка игры"
		:src="game.image_url"/>

		<div class="info_container">
			<p class="title">{{ game.title }}</p>
			<p v-if="game.min_price_discount == 0">бесплатно</p>
			<p v-else>
				от
				<span class="min_price--highlighted">{{ game.min_price_discount }}₽</span>
			</p>
		</div>
	</div>
</template>

<style scoped>
.game_card {
	--fs_info: 0.8rem;

	overflow: hidden;
	display: flex;
	flex-direction: column;
	width: 100%;
	background-color: var(--c_bg__surface);
	box-shadow:
		0 0.5rem 1.5rem rgba(0, 0, 0, 0.4),
		0 0.125rem 0.375rem rgba(0, 0, 0, 0.3);
}

.game_image {
	width: 100%;
	object-fit: cover;
	object-position: center;
	aspect-ratio: 2.14 / 1;
}

.info_container {
	--fs_info: 0.8rem;

	padding: 0.5rem;
	display: flex;
	flex-direction: column;
	justify-content: space-between;
	flex: 1;
	row-gap: var(--fs_info);
	font-size: var(--fs_info);
}

.title {
	display: -webkit-box;
	-webkit-box-orient: vertical;
	-webkit-line-clamp: 2;
	overflow: hidden;
	text-overflow: ellipsis;
}

.min_price--highlighted {
	font-size: 1rem;
}
</style>