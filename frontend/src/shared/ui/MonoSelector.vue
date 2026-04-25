<script setup lang="ts" generic="T">
import LoadIndicator from "@/shared/ui/LoadIndicator.vue"
import type { SelectorValue } from "../interface/Filters"
import { ref } from "vue"

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

const handleOptionClick = (name: string, option: SelectorValue<T>) => {
	props.onOptionClick(name, option)
	isOpen.value = !props.isAutoClose
}
</script>

<template>
	<div class="mono_selector">
		<button class="label_button" @click="isOpen = !isOpen" @blur="isOpen = false">
			<span class="label">{{ props.selectedOption?.title ?? props.label }}</span>
			<span class="arrow" :class="{ 'arrow--active': isOpen }">↓</span>
		</button>

		<div class="separator">
			<div class="options_container" v-show="isOpen">
				<template v-if="!props.isLoading && props.options.length">
					<div class="option" 
					:class="{ 'option--active': props.selectedOption?.title == option.title }"
					v-for="option in props.options" 
					:key="option.title"
					@mousedown.prevent="() => handleOptionClick(props.name, option)">
						{{ option.title }}
					</div>
				</template>

				<div class="load_container" v-else-if="props.isLoading">
					<LoadIndicator :is-short="true"/>
				</div>

				<div class="load_container" v-else>
					<p class="load_message">
						NO SIGNAL
					</p>
				</div>
			</div>
		</div>
	</div>
</template>

<style scoped>
.mono_selector {
	--fs_mono_selector: 1rem;

	display: flex;
	flex-direction: column;
	width: 100%;
	user-select: none;
}

.mock_selector {
	position: absolute;
	opacity: 0;
}

.label_button {
	padding: 0.5rem 1rem;
	display: grid;
	grid-template-columns: 1fr auto;
	width: 100%;
	background-color: var(--bc_mono_selector, var(--c_bg));
	font-size: var(--fs_mono_selector);
	color: var(--c_mono_selector, var(--c_text));
}

.label {
	text-overflow: ellipsis;
	white-space: nowrap;
	overflow: hidden;
}

.arrow {
	transition: transform 0.2s ease-out;
}
.arrow--active {
	transform: rotateX(-180deg);
}

.separator {
	position: relative;
	border-bottom: 0.25rem solid var(--c_secondary);
}

.options_container {
	z-index: 1;
	overflow-x: hidden;
	overflow-y: auto;
	position: absolute;
	width: 100%;
	height: 14.5rem;
	background-color: var(--c_bg);
	border: 0.25rem solid var(--c_secondary);
  	scrollbar-color: var(--c_text) var(--c_bg);
	scrollbar-width: thin;
}

.option {
	overflow: hidden;
	text-overflow: ellipsis;
	white-space: nowrap;
	padding: 0.5rem 1rem;
	width: 100%;
	font-size: calc(var(--fs_mono_selector) - 0.2rem);
	color: var(--c_text);
}
.option:hover {
	background-color: var(--c_bg__surface);
}
.option--active {
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

.load_message {
	font-size: var(--fs_multi_selector);
	text-decoration: underline;
	color: var(--c_placeholder);
	user-select: none;
}

@media (max-width: 1024px) {
	.label_button,
	.option {
		padding: 0.5rem 0.5rem;
	}
}
@media (max-width: 600px) {
	.mono_selector {
		--fs_mono_selector: 0.8rem;
	}
	.label_button,
	.option {
		padding: 0.5rem 0.25rem;
	}
}
</style>