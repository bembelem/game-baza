<script setup lang="ts">
import { toRefs, computed } from "vue"
import { useFormField } from "@/shared/lib/useFormField"

const props = defineProps<{
	name: string,
	type?: "text" | "email" | "tel",
	placeholder?: string,
	maxLength?: number,
	autoComplete?: string,
	formatInput?: (input: string) => string,
}>()

const { value, onBlur } = toRefs(useFormField(props.name))

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
	<input class="input"
	:name="props.name"
	:type="props.type ?? 'text'"
	:placeholder="props.placeholder"
	:maxlength="maxLength"
	:autocomplete="props.autoComplete ?? 'off'"
	v-model="proxyValue"
	@blur="onBlur"/>
</template>

<style scoped>
.input {
	padding: 0.5rem;
	width: 100%;
	border: 0.25rem solid var(--bc_input_field, var(--c_secondary));
	background-color: var(--c_bg__surface);
	transition: border-color 0.2s ease-in-out;
}
.input::placeholder {
	color: var(--c_placeholder);
}
.input:focus {
	border-color: var(--bc_input_field__focus, var(--c_secondary__accent));
}
</style>