<script setup lang="ts">
import { ref, onMounted, nextTick, watch } from "vue"
import SkeletonLoader from "./SkeletonLoader.vue"

const { skeletonLines = 4, ...props } = defineProps<{
	skeletonLines?: number
	description?: string
}>()

const isActive = ref(false)
const isOverflow = ref(false)
const textRef = ref<HTMLElement>()

function checkOverflow() {
	if (!textRef.value) return

	isOverflow.value = textRef.value.scrollHeight > textRef.value.clientHeight
}

function toggleExpanded() {
	isActive.value = !isActive.value
}

onMounted(async () => {
	await nextTick()
	checkOverflow()
})

watch(() => props.description, async () => {
	await nextTick()
	checkOverflow()
})
</script>

<template>
	<div class="description">
		<template v-if="props.description">
			<p
			ref="textRef"
			class="text"
			:class="{ 'text--active': isActive }">
				{{ props.description }}
			</p>

			<button
			v-if="isOverflow || isActive"
			class="button_read_all"
			@click="toggleExpanded">
				{{ isActive ? "скрыть" : "читать полностью" }}
			</button>
		</template>

		<div
		v-else
		class="skeleton_container">
			<SkeletonLoader
			v-for="i in skeletonLines"
			:key="i"
			class="text_skeleton"
			:style="{ '--i': i }"/>
		</div>
	</div>
</template>

<style scoped>
.description {
	--fs: var(--fs_description_section, var(--fs__md));
	--lh: var(--lh_description_section, var(--lh_global));

	display: flex;
	flex-direction: column;
	align-items: flex-start;
	padding: var(--space__sm) var(--space__lg);
	width: 100%;
	border: var(--border__md) solid var(--c_bg__surface);
	color: var(--c_text__primary);
	font-size: var(--fs);
	line-height: var(--lh);
}

.text {
	display: -webkit-box;
	overflow: hidden;
	-webkit-line-clamp: 4;
	-webkit-box-orient: vertical;
}
.text--active {
	display: block;
	overflow-wrap: anywhere;
}

.button_read_all {
	padding: 0;
	background-color: transparent;
	font-size: calc(var(--fs) - 0.1rem);
	color: var(--c_brand__purple_bright);
	cursor: pointer;
	user-select: none;
}

.skeleton_container {
	display: flex;
	flex-direction: column;
	width: 100%;
}

.text_skeleton {
	--h_skeleton_loader: calc(var(--fs) * var(--lh));

	animation-duration: var(--ad_description_section, 1.5s);
	animation-delay: calc(var(--i, 1) * var(--skeleton_step, 0.15s));
}
</style>