<script lang="ts" setup>
import { ref } from "vue"
import EyeIcon from "@/assets/icons/interface-essential-view-eye--Streamline-Pixel.svg?component"
import { useFormField } from "@/shared/lib/useFormField"

const props = defineProps<{
	name: string
	placeholder?: string
	autoComplete?: "current-password" | "new-password"
	onBlur?: () => void
}>()

const { value, onBlur } = useFormField(props.name)
const isVisible = ref(false)

function handleSwitchVisible() {
	isVisible.value = !isVisible.value
}
</script>

<template>
	<div class="password_input">
		<input
		v-model="value"
		class="input"
		:type="isVisible ? 'text' : 'password'"
		:placeholder="placeholder"
		:autocomplete="autoComplete"
		@blur="onBlur"/>

		<button
		v-if="isVisible"
		class="icon_button"
		type="button"
		@click="handleSwitchVisible">
			<EyeIcon class="icon"/>
		</button>

		<button
		v-else
		class="icon_button"
		type="button"
		@click="handleSwitchVisible">
			<EyeIcon class="icon" />
			<span class="line">/</span>
		</button>
	</div>
</template>

<style scoped>
.password_input {
	display: flex;
	align-items: center;
	border: var(--border__md) solid var(--bc_password_field, var(--c_brand__purple));
	background-color: var(--c_bg__surface);
	transition: border-color 0.2s ease-in-out;
}
.password_input:focus-within {
	border-color: var(--bc_password_field__focus, var(--c_brand__purple_bright));
}

.input {
	width: 100%;
	background-color: var(--c_bg__surface);
}
.input::placeholder {
	color: var(--c_text__muted);
}

.icon_button {
	position: relative;
	padding: 0 var(--space__sm);
	background-color: transparent;
	color: var(--c_text__primary);
}

.icon {
	width: var(--fs__md);
	height: var(--fs__md);
}

.line {
	position: absolute;
	top: 50%;
	left: 50%;
	transform: translateX(-50%) translateY(-50%);
}
</style>