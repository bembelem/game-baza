<script setup lang="ts">
const props = defineProps<{
	label?: string,
	error?: string
}>()
</script>

<template>
	<div class="form_field">
		<label>
			<p class="label">{{ props.label }}</p>
			<slot></slot>
		</label>
		<p class="error">{{ props.error }}</p>
	</div>
</template>

<style scoped>
.form_field {
	display: flex;
	flex-direction: column;
}

.label {
	margin-bottom: 0.25rem;
	font-size: 0.875rem;
}

.error {
	margin-top: 0.25rem;
	min-height: 0.75rem;
	font-size: 0.75rem;
	color: var(--c_text__error);
}
</style>