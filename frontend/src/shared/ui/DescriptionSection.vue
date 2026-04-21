<script setup lang="ts">
import SkeletonLoader from "./SkeletonLoader.vue"
import { ref, onMounted, nextTick, watch } from "vue"

const { skeletonLines = 5, ...props } = defineProps<{ 
	skeletonLines?: number
	description?: string,
}>()

const isActive = ref(false)
const isOverflow = ref(false)
const textRef = ref<HTMLElement>()

const checkOverflow = () => {
	if (!textRef.value) return

	isOverflow.value = textRef.value.scrollHeight > textRef.value.clientHeight
}

onMounted(async () => {
	await nextTick()
	checkOverflow()
})

watch(() => props.description, async () => {
	await nextTick()
	checkOverflow()
})

const toggleExpanded = () => { isActive.value = !isActive.value }
</script>

<template>
	<div class="description">
		<template v-if="props.description">
			<p class="text" :class="{ 'text--active': isActive }" ref="textRef">
				{{ props.description }}
			</p>

			<button class="button_read_all" @click="toggleExpanded" v-if="isOverflow || isActive">
				{{ isActive ? "скрыть" : "читать полностью" }}
			</button>
		</template>

		<div v-else class="skeleton_container">
			<SkeletonLoader v-for="i in skeletonLines" :key="i"
			class="text_skeleton"
			:style="{ '--i': i }"/>
		</div>
	</div>
</template>

<style scoped>
.description {
	--fs: var(--fs_description_section, 1rem);
	--lh: var(--lh_description_section, 1.6);

	display: flex;
	flex-direction: column;
	width: 100%;
	padding: 1.25rem 1.5rem;
	align-items: flex-start;
	border: 0.25rem solid var(--c_bg__surface);
	color: var(--c_text__muted);
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
	color: var(--c_secondary__accent);
	font-size: calc(var(--fs) - 0.1rem);
	cursor: pointer;
	user-select: none;
}

.skeleton_container {
	display: flex;
	flex-direction: column;
	gap: calc(var(--fs) * var(--lh) - var(--fs));
	width: 100%;
}

.text_skeleton {
	--h_skeleton_loader: var(--fs);
	animation-duration: var(--ad_description_section, 1.5s);
	animation-delay: calc(var(--i, 1) * var(--skeleton_step, 0.15s));
}
</style>