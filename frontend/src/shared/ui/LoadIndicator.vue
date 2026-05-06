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
	font-size: var(--fs_load, var(--fs__md));
	color: var(--c_load, var(--c_brand__purple));
	white-space: nowrap;
	animation: loading var(--ad_loading) infinite ease-in-out;
}
@keyframes loading {
	50% {
		color: var(--c_load__accent, var(--c_brand__purple_bright));
	}
}

.dot_1, .dot_2, .dot_3 {
	display: inline-block;
	animation: dots var(--ad_loading) infinite ease-in-out; 
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