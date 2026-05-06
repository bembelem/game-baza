<script setup lang="ts" generic="T">
import { ref } from "vue"
import LoadIndicator from "@/shared/ui/LoadIndicator.vue"
import type { SelectorValue } from "../interface/Filters"

const props = defineProps<{
	name: string,
	selectedOptions: SelectorValue<T>[] | undefined,
	options: SelectorValue<T>[],
	label?: string,
	isLoading?: boolean,
	isAutoClose?: boolean,
	onOptionClick: (name: string, option: SelectorValue<T>[]) => void
}>()

const isOpen = ref(false)

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
	<div class="multi_selector">
		<button
		class="label_button"
		@click="isOpen = !isOpen"
		@blur="isOpen = false">
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
					v-for="option in props.options"
					:key="option.title"
					class="option"
					:class="{ 'option--active': props.selectedOptions?.some((selectedOption) => selectedOption.title == option.title) }"
					@mousedown.prevent="() => handleOptionClick(props.name, option)">
						{{ option.title }}
					</div>
				</template>

				<div
				v-else-if="props.isLoading"
				class="load_container">
					<LoadIndicator :is-short="true"/>
				</div>

				<div
				v-else
				class="load_container">
					<p class="load_message">NO SIGNAL</p>
				</div>
			</div>
		</div>
	</div>
</template>

<style scoped>
.multi_selector {
	display: flex;
	flex-direction: column;
	font-size: var(--fs__md);
	user-select: none;
}

.label_button {
	display: grid;
	grid-template-columns: 1fr auto;
	gap: var(--space__sm);
	padding: var(--space__sm);
	background-color: var(--bc_multi_selector, var(--c_bg__primary));
	font-size: inherit;
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
	position: absolute;
	z-index: 1;
	overflow-x: hidden;
	overflow-y: auto;
	width: 100%;
	height: calc((var(--lh_global) * var(--fs__sm) + var(--space__sm) * 2) * 5 + var(--border__md) * 2);
	border: var(--border__md) solid var(--c_brand__purple);
	background-color: var(--c_bg__primary);
	scrollbar-color: var(--c_text__muted) var(--c_bg__primary);
	scrollbar-width: thin;
}

.option {
	overflow: hidden;
	text-overflow: ellipsis;
	white-space: nowrap;
	width: 100%;
	padding: var(--space__sm);
	font-size: var(--fs__sm);
	color: var(--c_text__primary);
}
.option:hover {
  	background-color: var(--c_bg__surface);
}
.option--active {
  	color: var(--c_brand__purple_bright);
}

.load_container {
	--fs_load: var(--fs_md);
	--c_load: var(--c_brand__purple);
	--c_load__accent: var(--c_brand__purple);

	display: flex;
	justify-content: center;
	align-items: center;
	height: 100%;
	font-size: var(--fs__md);
}

.load_message {
	color: var(--c_text__muted);
	text-decoration: underline;
}
</style>