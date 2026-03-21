<script setup lang="ts">
import { ref } from "vue"
import EyeIcon from "@/assets/icons/interface-essential-view-eye--Streamline-Pixel.svg?component"

const value = defineModel()
const props = defineProps<{
	placeholder?: string
}>()
const isVisible = ref(false)

const handleSwitchVisible = () => { isVisible.value = !isVisible.value }
</script>

<template>
	<div class="password_input">
		<input class="input" 
		:type=" isVisible ? 'text' : 'password'"
		:placeholder="props.placeholder"
		v-model="value"/>
		
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
.password_input,
.password_input__error {
	box-sizing: border-box;
	padding: 0.5rem;
	display: flex;
	align-items: center;
	width: 100%;
	border: 0.25rem solid var(--c_secondary);
	background-color: var(--c_bg__surface);
	transition: border-color 0.2s ease-in-out;
}
.password_input__error {
	border-color: var(--c_error);
}
.password_input:focus-within,
.password_input__error:focus-within {
	border-color: var(--c_secondary__accent);
}

.input {
	width: 100%;
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