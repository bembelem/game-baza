<script lang="ts" setup>
import { computed } from "vue"
import { useFormField } from "@/shared/lib/useFormField"

const props = defineProps<{
	name: string
	type?: "text" | "email" | "tel"
	placeholder?: string
	maxLength?: number
	autoComplete?: string
	formatInput?: (input: string) => string
}>()

const { value, onBlur } = useFormField(props.name)

const proxyValue = computed({
	get() {
		if (!value.value) return ""

		return props.formatInput
			? props.formatInput(value.value)
			: value.value
	},
	set(input: string) {
		value.value = input
	}
})
</script>

<template>
	<input
	v-model="proxyValue"
	class="input"
	:name="name"
	:type="type ?? 'text'"
	:placeholder="placeholder"
	:maxlength="maxLength"
	:autocomplete="autoComplete ?? 'off'"
	@blur="onBlur"/>
</template>

<style scoped>
.input {
	width: 100%;
	border: var(--border__md) solid var(--bc_input_field, var(--c_brand__purple));
	background-color: var(--c_bg__surface);
	transition: border-color 0.2s ease-in-out;
}
.input::placeholder {
	color: var(--c_text__muted);
}
.input:focus {
	border-color: var(--bc_input_field__focus, var(--c_brand__purple_bright));
}
</style>