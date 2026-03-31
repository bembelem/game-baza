<script setup lang="ts">
const props = defineProps<{
	label?: string,
	error?: string,
	isValid?: boolean,
	onBlur?: () => void
}>()
</script>

<template>
	<div class="form_field" 
	:class="{ 'form_field--fulfilled': props.isValid, 'form_field--error': props.error }">
		<label @blur="props.onBlur">
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
.form_field--error {
	--bc_input_field: var(--c_error);
	--bc_password_field: var(--c_error);
}
.form_field--fulfilled {
	--bc_input_field: var(--bc_input_field__focus);
	--bc_password_field: var(--bc_password_field__focus);
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