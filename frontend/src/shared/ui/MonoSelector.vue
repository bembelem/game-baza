<script setup lang="ts" generic="T">
import { ref } from "vue"
import LoadIndicator from "@/shared/ui/LoadIndicator.vue"
import type { SelectorValue } from "../interface/Filters"

const props = withDefaults(defineProps<{
	name: string,
	selectedOption: SelectorValue<T> | undefined,
	options: SelectorValue<T>[],
	label?: string,
	isLoading?: boolean,
	isAutoClose?: boolean,
	onOptionClick: (name: string, option: SelectorValue<T>) => void
}>(), {
	label: "выбрать",
	isAutoClose: true
})

const isOpen = ref(false)

function handleOptionClick(name: string, option: SelectorValue<T>) {
	props.onOptionClick(name, option)
	isOpen.value = !props.isAutoClose
}
</script>

<template>
	<div class="mono_selector">
		<button
		class="label_button"
		@click="isOpen = !isOpen"
		@blur="isOpen = false">
			<span class="label">{{ props.selectedOption?.title ?? props.label }}</span>
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
					:class="{ 'option--active': props.selectedOption?.title == option.title }"
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
.mono_selector {
	display: flex;
	flex-direction: column;
	width: 100%;
	user-select: none;
}

.label_button {
	display: grid;
	grid-template-columns: 1fr auto;
	gap: var(--space__sm);
	width: 100%;
	padding: var(--space__sm);
	background-color: var(--bc_mono_selector, var(--c_bg__primary));
	color: var(--c_mono_selector, var(--c_text__primary));
}

.label {
	overflow: hidden;
	text-overflow: ellipsis;
	white-space: nowrap;
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
	scrollbar-color: var(--c_text__primary) var(--c_bg__primary);
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
	--c_load: var(--c_brand__purple);
	--c_load__accent: var(--c_brand__purple);

	display: flex;
	justify-content: center;
	align-items: center;
	height: 100%;
}

.load_message {
	color: var(--c_text__muted);
	text-decoration: underline;
	user-select: none;
}
</style>