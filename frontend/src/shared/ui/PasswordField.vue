<script setup lang="ts">
import EyeIcon from "@/assets/icons/interface-essential-view-eye--Streamline-Pixel.svg?component"
import { toRefs, ref } from "vue"
import { useFormField } from "@/shared/lib/useFormField"

const props = defineProps<{
	name: string,
	placeholder?: string,
	autoComplete?: "current-password" | "new-password",
	onBlur?: () => void
}>()

const { value, onBlur } = toRefs(useFormField(props.name))
const isVisible = ref(false)

const handleSwitchVisible = () => { isVisible.value = !isVisible.value }
</script>

<template>
	<div class="password_input">
		<input class="input" 
		:type=" isVisible ? 'text' : 'password'"
		:placeholder="props.placeholder"
		:autocomplete="props.autoComplete"
		v-model="value"
		@blur="onBlur"/>
		
		<button class="icon_button" type="button" v-if="isVisible" @click="handleSwitchVisible">
			<EyeIcon class="icon"/>
		</button>
		
		<button class="icon_button" type="button" @click="handleSwitchVisible" v-else>
			<EyeIcon class="icon"/>
			<span class="line">/</span>
		</button>
	</div>
</template>

<style scoped>
.password_input {
	box-sizing: border-box;
	padding: 0.5rem;
	display: flex;
	align-items: center;
	width: 100%;
	border: 0.25rem solid var(--bc_password_field, var(--c_secondary));
	background-color: var(--c_bg__surface);
	transition: border-color 0.2s ease-in-out;
}
.password_input:focus-within {
	border-color: var(--bc_password_field__focus, var(--c_secondary__accent));
}

.input {
	width: 100%;
	background-color: var(--c_bg__surface);
}
.input::placeholder {
	color: var(--c_placeholder);
}

.icon {
	height: 1rem;
	width: 1rem;
}
.icon_button {
	position: relative;
	padding: 0;
	color: var(--c_text);
	background-color: transparent;
}

.line {
	position: absolute;
	top: 50%;
	left: 50%;
	transform: translateX(-50%) translateY(-50%);
}
</style>