<script setup lang="ts">
import SearchIcon from "@/assets/icons/interface-essential-search-1--Streamline-Pixel.svg?component"

const props = defineProps<{
	placeholder: string,
	onSearch: () => void
}>()

const searchInput = defineModel()
</script>

<template>
  	<div class="search_bar">
		<input
		class="search_input"
		type="search"
		v-model="searchInput"
		:placeholder="props.placeholder"/>

		<button
		class="search_button"
		@click="props.onSearch">
			<SearchIcon class="icon"/>
		</button>
	</div>
</template>

<style scoped>
.search_bar {
	display: flex;
	justify-self: center;
	width: 100%;
}

.search_input {
	width: 100%;
	padding: var(--space__xs) var(--space__md);
	border: var(--border__md) solid var(--c_brand__purple);
	border-right: none;
	background-color: var(--c_bg__surface);
	transition: border-color 0.2s ease-in-out;
}
.search_input::placeholder {
  	color: var(--c_text__muted);
}
.search_input:focus {
  	border-color: var(--c_brand__purple_bright);
}

.search_button {
	border: var(--border__md) solid var(--c_brand__purple_bright);
	background-color: var(--c_brand__purple_bright);
	color: var(--c_bg__primary);
	transition: color 0.2s ease-out;
}
.search_button:active {
  	color: var(--c_text__primary);
}

.icon {
  	width: var(--fs__xl);
  	height: var(--fs__xl);
}
</style>