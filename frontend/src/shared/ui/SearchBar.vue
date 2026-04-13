<script setup lang="ts">
import SearchIcon from "@/assets/icons/interface-essential-search-1--Streamline-Pixel.svg?component"

const searchInput = defineModel()
const props = defineProps<{ 
	placeholder: string,
	onSearch: () => void 
}>()
</script>

<template>
	<div class="search_bar">
		<input class="search_input" 
		type="search" 
		v-model="searchInput"
		:placeholder="props.placeholder"/>	

		<button class="search_button" @click="props.onSearch">
			<SearchIcon class="icon"/>
		</button>
	</div>
</template>

<style scoped>
.search_bar {
	justify-self: center;
	box-sizing: border-box;
	display: flex;
	column-gap: 0.5rem;
	width: 100%;
}

.search_input {
	padding: 0.5rem;
	width: 100%;
	border: 0.25rem solid var(--c_secondary);
	background-color: var(--c_bg__surface);
	transition: border-color 0.2s ease-in-out;
}
.search_input::placeholder {
	color: var(--c_placeholder);
}
.search_input:focus {
	border-color: var(--c_secondary__accent);
}

.search_button {
	border: 0.25rem solid var(--c_secondary__accent);
	background-color: var(--c_secondary__accent);
	color: var(--c_bg);
	transition: color 0.2s ease-out;
}
.search_button:active {
	color: var(--c_text);
}

.icon {
	width: 1.5rem;
	height: 1.5rem;
}
</style>