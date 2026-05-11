<script lang="ts" setup>
const props = defineProps<{
	label?: string
	error?: string
	isValid?: boolean
	onBlur?: () => void
}>()
</script>

<template>
	<div
	class="form_field"
	:class="{
		'form_field--fulfilled': isValid,
		'form_field--error': error
	}">
		<label @blur="props.onBlur">
			{{ label }}
			<slot/>
		</label>
		<p class="error">{{ error }}</p>
	</div>
</template>

<style scoped>
.form_field {
	display: flex;
	flex-direction: column;
	gap: var(--space__xs);
	font-size: var(--fs__sm);
}
.form_field--error {
	--bc_input_field: var(--c_error);
	--bc_password_field: var(--c_error);
}
.form_field--fulfilled {
	--bc_input_field: var(--bc_input_field__focus);
	--bc_password_field: var(--bc_password_field__focus);
}

.error {
	min-height: calc(var(--fs__sm) * var(--lh_global));
	color: var(--c_text__error);
}
</style>