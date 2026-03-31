<script setup lang="ts">
const props = defineProps<{ isShort: boolean }>()
</script>

<template>
	<p class="loading_indicator">
		<template v-if="!props.isShort">Loading</template>
		<span class="dot_1">.</span>					
		<span class="dot_2">.</span>	     						
		<span class="dot_3">.</span>
	</p>
</template>

<style scoped>
.loading_indicator {
	--ad_loading: 1.2s;

	display: inline;
	font-size: var(--fs_load, 2rem);
  	color: var(--c_load, var(--c_secondary));
	white-space: nowrap;

	animation-name: loading;
	animation-duration: var(--ad_loading);
	animation-iteration-count: infinite;
	animation-timing-function: ease-in-out;
}
@keyframes loading {
	50% {
		color: var(--c_load__accent, var(--c_secondary__accent));
	}
}

.dot_1, .dot_2, .dot_3 {
	display: inline-block;
	animation-name: dots;
	animation-duration: var(--ad_loading);
	animation-iteration-count: infinite;
	animation-timing-function: ease-in-out;
}
.dot_2 {
	animation-delay: calc(var(--ad_loading) / 3);
}
.dot_3 {
	animation-delay: calc(var(--ad_loading) / 3 * 2);
}
@keyframes dots {
	0%, 50%, 100% {
		transform: translateY(0);
	}
	25% {
		transform: translateY(-100%);
	}
}
</style>