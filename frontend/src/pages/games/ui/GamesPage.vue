<script setup lang="ts">
import { useTemplateRef } from "vue"
import GamesFilters from "@/widgets/games_filters/ui/GamesFilters.vue"
import GamesCatalog from "@/widgets/games_catalog/ui/GamesCatalog.vue"
import LoadIndicator from "@/shared/ui/LoadIndicator.vue"
import { useSearchGamesStore } from "@/features/search_games/store/searchGamesStore"

const { gamesStore } = useSearchGamesStore()

const gamesCatalogRef = useTemplateRef<HTMLElement>("games_count")

function handleFloatedButtonClick() {
	gamesCatalogRef.value?.scrollIntoView({
		behavior: "smooth",
		block: "center"
	})
}
</script>

<template>
	<section class="games_catalog">
		<h2
		ref="games_count"
		class="games_count">
			КАТАЛОГ ИГР
			<span class="games_count--highlighted">
				<LoadIndicator
				v-if="gamesStore.isPending.value"
				class="load"
				:is-short="true"/>

				<template v-else>
					{{ gamesStore.data.value?.total }}
				</template>
			</span>
		</h2>
		<GamesFilters/>
		<GamesCatalog/>
	</section>

	<button
	class="floated_button"
	@click="handleFloatedButtonClick">
		↑
	</button>
</template>

<style scoped>
.games_catalog {
	display: flex;
	flex-direction: column;
	gap: var(--space__2xl);
	padding: var(--space__3xl) 0;
}

.games_count {
	--fs_load: var(--fs__2xl);

	font-size: var(--fs__2xl);
	color: var(--c_text__primary);
}
.games_count--highlighted {
  	color: var(--c_brand__gold_bright);
}

.load {
	--c_load: var(--c_brand__gold_bright);
	--c_load__accent: var(--c_brand__gold_bright);
}

.floated_button {
	position: fixed;
	bottom: var(--p_layout);
	right: var(--p_layout);
	width: var(--space__3xl);
	height: var(--space__3xl);
	background-color: var(--c_bg__primary);
	box-shadow: var(--neon__purple);
	font-size: var(--fs__2xl);
	color: var(--c_brand__purple_bright);
	cursor: pointer;
}
</style>