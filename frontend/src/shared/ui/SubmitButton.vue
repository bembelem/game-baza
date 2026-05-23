<script lang="ts" setup>
import LoadIndicator from "./LoadIndicator.vue"

const props = withDefaults(defineProps<{
	label: string
	type?: "submit" | "button" | "reset" 
	isSubmitting?: boolean
	isAvailable?: boolean
}>(), {
	type: "submit",
	isAvailable: true
})
</script>

<template>
	<button
		class="submit_button"
		:class="{
			'submit_button--fulfilled': props.isAvailable,
			'submit_button--submitted': props.isSubmitting
		}"
		:type="props.type"
		:disabled="!props.isAvailable || props.isSubmitting">

		<LoadIndicator
		v-if="props.isSubmitting"
		class="load"
		is-short/>

		<p v-else>{{ props.label }}</p>
	</button>
</template>

<style scoped>
.submit_button {
	padding: var(--space__xs);
	width: 100%;
	border: var(--border__md) solid var(--bc_submit_button, var(--c_brand__purple));
	background-color: var(--bc_submit_button, var(--c_brand__purple));
	transition:
		background-color 0.2s ease-in-out,
		border-color 0.2s ease-in-out;
}
.submit_button:disabled {
	color: var(--c_bg__primary);
}
.submit_button--fulfilled {
	border-color: var(--bc_submit_button__accent, var(--c_brand__purple_bright));
	background-color: var(--bc_submit_button__accent, var(--c_brand__purple_bright));
}
.submit_button--submitted:disabled {
	border-color: var(--c_text__muted);
	background-color: transparent;
	color: var(--c_text__muted);
}

.load {
	--c_load: var(--c_text__muted);
	--c_load__accent: var(--c_text__muted);
}
</style>