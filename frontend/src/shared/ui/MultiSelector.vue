<script setup lang="ts" generic="T">
import { ref, computed } from "vue"
import SearchBar from "./SearchBar.vue"
import LoadIndicator from "@/shared/ui/LoadIndicator.vue"
import type { SelectorValue } from "../interface/Filters"

const props = withDefaults(defineProps<{
	name: string,
	selectedOptions: SelectorValue<T>[] | undefined,
	options: SelectorValue<T>[],
	label?: string,
	isLoading?: boolean,
	isAutoClose?: boolean,
	hasSearch?: boolean,
	onOptionClick: (name: string, option: SelectorValue<T>[]) => void
}>(), {
	hasSearch: true
})

const isOpen = ref(false)
const searchValue = ref("")

const filteredOptions = computed(() => {
	if (!searchValue.value) return props.options

	return props.options.filter((option) => option.title.toLowerCase().includes(searchValue.value.toLowerCase()))
})

function handleOptionClick(name: string, newOption: SelectorValue<T>) {
	const newOptions = props.selectedOptions ? [...props.selectedOptions] : []
	const optionIndex = newOptions.findIndex((option) => option.title == newOption.title)

	if (optionIndex == -1) {
		newOptions.push(newOption)
	} else {
		newOptions.splice(optionIndex, 1)
	}

	props.onOptionClick(name, newOptions)
	isOpen.value = !props.isAutoClose
}
</script>

<template>
	<div 
	class="multi_selector"
	tabindex="-1"
	@focusout="(e) => { if (!$el.contains(e.relatedTarget)) isOpen = false }">
		<button
		class="label_button"
		@click="isOpen = !isOpen">
			<div class="label_container">
				<span class="label">{{ props.label }}</span>
				<span v-if="props.selectedOptions?.length">
					|
					<span class="selected_count">{{ props.selectedOptions.length }}</span>
				</span>
			</div>
			<span
			class="arrow"
			:class="{ 'arrow--active': isOpen }">
				↓
			</span>
		</button>

		<div class="separator">
			<div
			v-show="isOpen"
			class="options_container">
				<template v-if="!props.isLoading && props.options.length">
					<div 
					v-if="props.hasSearch"
					class="search_bar">
						<SearchBar 
						v-model="searchValue"
						placeholder="Поиск..."/>
					</div>

					<template v-if="filteredOptions.length">
						<button
						v-for="option in filteredOptions"
						:key="option.title"
						class="option"
						:class="{ 'option--active': props.selectedOptions?.some((selectedOption) => selectedOption.title == option.title) }"
						@click="() => handleOptionClick(props.name, option)">
							{{ option.title }}
						</button>
					</template>

					<p 
					v-else 
					class="data_message data_message--text">
						NO RESULTS
					</p>
				</template>
				
				<LoadIndicator 
				v-else-if="props.isLoading"
				class="data_message" 
				:is-short="true"/>

				<p 
				v-else 
				class="data_message data_message--text">
					NO SIGNAL
				</p>
			</div>
		</div>
	</div>
</template>

<style scoped>
.multi_selector {
	display: flex;
	flex-direction: column;
	user-select: none;
}

.label_button {
	display: grid;
	grid-template-columns: 1fr auto;
	gap: var(--space__sm);
	padding: var(--space__sm);
	background-color: var(--bc_multi_selector, var(--c_bg__primary));
	color: var(--c_multi_selector, var(--c_text__primary));
}

.label_container {
  	display: grid;
  	grid-template-columns: 1fr auto;
}

.label {
	overflow: hidden;
	text-overflow: ellipsis;
	white-space: nowrap;
}

.selected_count {
  	color: var(--c_brand__gold_bright);
}

.arrow {
  	transition: transform 0.2s ease-out;
}
.arrow--active {
  	transform: rotateX(-180deg);
}

.separator {
	position: relative;
	border-bottom: var(--border__md) solid var(--c_brand__purple);
}

.options_container {
	--b_search_input: none;
	--b_search_button: none;
	--p_search_input: var(--space__sm);
	--fs_search_input: var(--fs__sm);
	--c_load: var(--c_brand__purple);
	--c_load__accent: var(--c_brand__purple);

	position: absolute;
	z-index: 1;
	display: flex;
	flex-direction: column;
	overflow-x: hidden;
	overflow-y: auto;
	width: 100%;
	height: calc((var(--lh_global) * var(--fs__sm) + var(--space__sm) * 2) * 5 + var(--border__md) * 2);
	border: var(--border__md) solid var(--c_brand__purple);
	background-color: var(--c_bg__primary);
	scrollbar-gutter: stable;
	scrollbar-width: thin;
	scrollbar-color: var(--c_text__primary) var(--c_bg__primary);
}

.search_bar {
	position: sticky;
	top: 0;
}

.option {
	flex-shrink: 0;
	overflow: hidden;
	text-overflow: ellipsis;
	white-space: nowrap;
	width: 100%;
	padding: var(--space__sm);
	font-size: var(--fs__sm);
	color: var(--c_text__primary);
	background-color: transparent;
	text-align: left;
}
.option:hover {
  	background-color: var(--c_bg__surface);
}
.option--active {
  	color: var(--c_brand__purple_bright);
}

.data_message {
	margin: auto;
}
.data_message--text {
	color: var(--c_text__muted);
	text-decoration: underline;
}
</style>