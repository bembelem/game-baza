<script setup lang="ts">
const value = defineModel()
const props = defineProps<{
	type?: "text" | "email" | "tel",
	placeholder?: string
}>()
</script>

<template>
	<input class="input" 
	:type="props.type ?? 'text'"
	:placeholder="props.placeholder"
	v-model="value"/>
</template>

<style scoped>
.input,
.input__error {
	padding: 0.5rem;
	width: 100%;
	border: 0.25rem solid var(--c_secondary);
	background-color: var(--c_bg__surface);
	transition: border-color 0.2s ease-in-out;
}
.input::placeholder,
.input__error::placeholder {
	color: var(--c_placeholder);
}
.input:focus,
.input__error:focus {
	border-color: var(--c_secondary__accent);
}
.input__error {
	border-color: var(--c_error);
}
</style>