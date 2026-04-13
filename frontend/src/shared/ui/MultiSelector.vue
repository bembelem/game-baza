<script setup lang="ts" generic="T">
import LoadIndicator from "@/shared/ui/LoadIndicator.vue"
import type { SelectorValue } from "../interface/Filters"
import { ref } from "vue"

const props = defineProps<{
	name: string,
	selectedValues: SelectorValue<T>[] | undefined,
	values?: SelectorValue<T>[] | null,
	label?: string,
	isAutoClose?: boolean,
	onValueClick: (name: string, value: SelectorValue<T>[]) => void
}>()

const isOpen = ref(false)

const handleValueClick = (name: string, newValue: SelectorValue<T>) => {
	const newValues = props.selectedValues ? [...props.selectedValues] : []
	const valueIndex = newValues.findIndex((value) => value.title == newValue.title)

	if (valueIndex == -1) {
		newValues.push(newValue)
	} else {
		newValues.splice(valueIndex, 1)
	}
	
	props.onValueClick(name, newValues)
	isOpen.value = !props.isAutoClose
}
</script>

<template>
	<div class="multi_selector">
		<button class="label_button" @click="isOpen = !isOpen" @blur="isOpen = false">
			<div class="label_container">
				<span class="label">{{ props.label }}</span>
				<span v-if="props.selectedValues?.length">
					|
					<span class="selected_count">{{ props.selectedValues.length }}</span>
				</span>
			</div>
			<span class="arrow" :class="{ 'arrow--active': isOpen }">↓</span>
		</button>

		<div class="separator">
			<div class="values_container" v-show="isOpen">
				<template v-if="props.values">
					<div class="value"
					:class="{ 'value--active': props.selectedValues?.some((selectedValue) => selectedValue.title == value.title) }"
					v-for="value in props.values" 
					:key="value.title"
					@mousedown.prevent="() => handleValueClick(props.name, value)">
						{{ value.title }}
					</div>
				</template>

				<div v-else class="load_container">
					<LoadIndicator :is-short="true"/>
				</div>
			</div>
		</div>
	</div>
</template>

<style scoped>
.multi_selector {
	--fs_multi_selector: 1rem;

	display: flex;
	flex-direction: column;
	width: 100%;
	user-select: none;
}

.label_button {
	padding: 0.5rem 1rem;
	display: grid;
	grid-template-columns: 1fr auto;
	column-gap: calc(var(--fs_multi_selector) / 2);
	width: 100%;
	background-color: var(--bc_multi_selector, var(--c_bg));
	font-size: var(--fs_multi_selector);
	color: var(--c_multi_selector, var(--c_text));
}

.label_container {
	display: grid;
	grid-template-columns: 1fr auto;
}

.label {
	text-overflow: ellipsis;
	white-space: nowrap;
	overflow: hidden;
}

.selected_count {
	color: var(--c_highlight__accent)
}

.arrow {
	transition: transform 0.2s ease-out;
}
.arrow--active {
	transform: rotateX(-180deg)
}

.separator {
	position: relative;
	border-bottom: 0.25rem solid var(--c_secondary);
}

.values_container {
	box-sizing: border-box;
	z-index: 1;
	overflow-x: hidden;
	overflow-y: auto;
	position: absolute;
	width: 100%;
	height: 15rem;
	background-color: var(--c_bg);
	border: 0.25rem solid var(--c_secondary);
	scrollbar-color: var(--c_placeholder) var(--c_bg);
	scrollbar-width: thin;
}

.value {
	box-sizing: border-box;
	overflow: hidden;
	text-overflow: ellipsis;
	white-space: nowrap;
	padding: 0.5rem 1rem;
	width: 100%;
	font-size: calc(var(--fs_multi_selector) - 0.2rem);
	color: var(--c_text);
}
.value:hover {
	background-color: var(--c_bg__surface);
}
.value--active {
	color: var(--c_secondary__accent);
}

.load_container {
	--c_load: var(--c_secondary);
	--c_load__accent: var(--c_secondary);

	display: flex;
	width: 100%;
	height: 100%;
	justify-content: center;
	align-items: center;
}

@media (max-width: 1024px) {
	.label_button,
	.value {
		padding: 0.5rem 0.5rem;
	}
}
@media (max-width: 600px) {
	.multi_selector {
		--fs_multi_selector: 0.8rem;
	}
	.label_button,
	.value {
		padding: 0.5rem 0.25rem;
	}
}
</style>