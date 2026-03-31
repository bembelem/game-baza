<script setup lang="ts">
import GamesCatalog from '@/widgets/games_catalog/ui/GamesCatalog.vue'
import LoadIndicator from '@/shared/ui/LoadIndicator.vue'
import { useTemplateRef } from 'vue'

const gamesCatalogRef = useTemplateRef<HTMLElement>("games_count")

const handleFloatedButtonClick = () => {
	gamesCatalogRef.value?.scrollIntoView({
		behavior: "smooth",
		block: "center"
	})
}
</script>

<template>
	<section class="games_catalog">
		<h2 class="games_count" ref="games_count">
			КАТАЛОГ ИГР
			<span class="games_count--highlighted">
				<LoadIndicator class="load" :is-short="true"/>
			</span>
		</h2>
		<GamesCatalog/>
	</section>
	
	<button class="floated_button" @click="handleFloatedButtonClick">↑</button>
</template>

<style scoped>
.games_catalog {
	margin-top: var(--h_header);
	padding: 4rem;
	display: flex;
	flex-direction: column;
	flex: 1;
}

.games_count {
	font-size: 2rem;
	color: var(--c_text);
}
.games_count--highlighted {
	color: var(--c_highlight__accent);
}

.load {
	--c_load: var(--c_highlight__accent);
	--c_load__accent: var(--c_highlight__accent); 
}

.floated_button {
	--fs_floated_button: 2rem;

	position: fixed;
	bottom: calc(var(--fs_floated_button) * 1.5);
	right: calc(var(--fs_floated_button) * 1.5);
	padding: calc(var(--fs_floated_button) / 2);
	background-color: var(--c_bg);
	box-shadow:
		0 0 0.375rem var(--c_secondary__accent),
		0 0 0.75rem var(--c_secondary__accent),
		0 0 1.125rem var(--c_secondary__accent),
		0 0 1.5rem var(--c_secondary__accent),
		0 0 1.875rem rgba(102, 0, 153, 0.4);
	font-size: var(--fs_floated_button);
	color: var(--c_secondary__accent);
	transition: color 0.1s ease-out,
				box-shadow 0.1s ease-out;
	cursor: pointer;
}

@media (max-width: 1024px) {
	.games_catalog {
		padding: 2rem;
	}
}
@media (max-width: 600px) {
	.games_catalog {
		padding: 1rem;
	}
	.games_count {
		font-size: 1.5rem;
	}
	.floated_button {
		--fs_floated_button: 1.5rem;
	}
}
</style>