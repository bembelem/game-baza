<script lang="ts" setup>
import GameInfo from "@/widgets/game_info/ui/GameInfo.vue"
</script>

<template>
	<div class="game_info_page">
		<GameInfo/>
	</div>
</template>

<style scoped>
.game_info_page {
	margin-top: var(--h_header);
	padding: 4rem;
	display: flex;
	flex-direction: column;
	flex: 1;
}

@media (max-width: 1024px) {
	.game_info_page {
		padding: 2rem;
	}
}
@media (max-width: 600px) {
	.game_info_page {
		padding: 1rem;
	}
}
</style>