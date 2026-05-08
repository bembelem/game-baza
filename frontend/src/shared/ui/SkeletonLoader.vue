<script setup lang="ts">
const { isLoading = true } = defineProps<{ isLoading?: boolean }>()
</script>

<template>
	<div class="text_skeleton" v-if="isLoading"></div>
	<slot v-else></slot>
</template>

<style scoped>
.text_skeleton {
	display: inline-block;
	width: var(--w_skeleton_loader, 100%);
	height: var(--h_skeleton_loader, var(--fs__md));
	background-color: var(--c_bg__surface);
	animation: skeleton 1s infinite;
}
@keyframes skeleton {
	50% {
		background-color: var(--c_bg__accent);
	}
	100% {
		background-color: var(--c_bg__surface);
	}
}
</style>