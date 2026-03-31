<script setup lang="ts">
import LoadIndicator from "./LoadIndicator.vue"

const props = defineProps<{
	label: string,
	isSubmitting?: boolean,
	isAvailable?: boolean
}>()
</script>

<template>
	<button class="submit_button" 
	:class="{ 'submit_button--fulfilled': props.isAvailable, 'submit_button--submitted': props.isSubmitting }" 
	type="submit"
	:disabled="!props.isAvailable || props.isSubmitting">
		<LoadIndicator class="load" :is-short="true" v-if="props.isSubmitting"/>
		<p v-else>{{ props.label }}</p>
	</button>
</template>

<style scoped>
.submit_button {
	margin-top: 1.75rem;
	padding: 0.5rem;
	border: 0.25rem solid var(--bc_submit_button, var(--c_secondary));
	background-color: var(--bc_submit_button, var(--c_secondary));
	transition: background-color 0.2s ease-in-out,
				border-color 0.2s ease-in-out;
}
.submit_button:disabled {
	color: var(--c_bg);
}
.submit_button--fulfilled {
	border-color: var(--bc_submit_button__accent, var(--c_secondary__accent));
	background-color: var(--bc_submit_button__accent, var(--c_secondary__accent));
}
.submit_button--submitted:disabled {
	border-color: var(--c_placeholder);
	background-color: transparent;
	color: var(--c_placeholder);
}

.load {
	--fs_load: 1rem;
  	--c_load: var(--c_placeholder);
	--c_load__accent: var(--c_placeholder);
}
</style>