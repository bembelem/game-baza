<script setup lang="ts" generic="T">
import LoadIndicator from "@/shared/ui/LoadIndicator.vue"
import type { SelectorValue } from "../interface/Filters"
import { ref } from "vue"

const props = withDefaults(defineProps<{
	name: string,
	value: SelectorValue<T> | undefined,
	values?: SelectorValue<T>[] | null,
	label?: string,
	isAutoClose?: boolean,
	onValueClick: (name: string, value: SelectorValue<T>) => void
}>(), {
	label: "выбрать",
	isAutoClose: true
})

const isOpen = ref(false)

const handleValueClick = (name: string, value: SelectorValue<T>) => {
	props.onValueClick(name, value)
	isOpen.value = !props.isAutoClose
}
</script>

<template>
	<div class="mono_selector">
		<button class="label_button" @click="isOpen = !isOpen" @blur="isOpen = false">
			<span class="label">{{ props.value?.title ?? props.label }}</span>
			<span class="arrow" :class="{ 'arrow--active': isOpen }">↓</span>
		</button>

		<div class="separator">
			<div class="values_container" v-show="isOpen">
				<template v-if="props.values">
					<div class="value" 
					:class="{ 'value--active': props.value?.title == value.title }"
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
	column-gap: 0.5rem;
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
  	scrollbar-color: var(--c_text) var(--c_bg);
	scrollbar-width: thin;
}

.value {
	box-sizing: border-box;
	overflow: hidden;
	text-overflow: ellipsis;
	white-space: nowrap;
	padding: 0.5rem 1rem;
	width: 100%;
	font-size: calc(var(--fs_mono_selector) - 0.2rem);
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
	.mono_selector {
		--fs_mono_selector: 0.8rem;
	}
	.label_button,
	.value {
		padding: 0.5rem 0.25rem;
	}
}
</style>