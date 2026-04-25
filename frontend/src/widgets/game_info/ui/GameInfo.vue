<script setup lang="ts">
import GameInfoMain from "./GameInfoMain.vue"
import SkeletonLoader from "@/shared/ui/SkeletonLoader.vue"
import DescriptionSection from "@/shared/ui/DescriptionSection.vue"
import type { GameFull } from "@/entities/game/model/Game"
import { type SearchGamesFilters, searchGamesFilters } from "@/features/search_games/filters/searchGamesFilters"
import { useRouter } from "vue-router"
import { computed } from "vue"
import { injectSearchGamesFilterOption } from "@/features/search_games/filters/searchGamesFiltersOptions"
import { Routes } from "@/shared/lib/router"

const router = useRouter()

const props = defineProps<{ gameInfo: Partial<GameFull> }>()

const { updateFilters, resetFilters } = searchGamesFilters

const date = computed(() => {
	if (!props.gameInfo.release_date) return

	const date = new Date(props.gameInfo.release_date)
  
	const options: Intl.DateTimeFormatOptions = {
		day: "numeric",
		month: "long",
		year: "numeric"
	}
	
	return date.toLocaleDateString("ru-RU", options)
})  

const handleMetadataClick = <K extends keyof SearchGamesFilters>(
	name: K,
	value: SearchGamesFilters[K]
) => {
	resetFilters()
	updateFilters(name, value)
	injectSearchGamesFilterOption(name, value)

	router.push({ name: Routes.games, query: { search: "true" } })
}
</script>

<template>
	<section class="game_info">
		<GameInfoMain :game-info="props.gameInfo"/>

		<div class="game_metadata game_metadata--genre">
			Жанр:
			<template v-if="props.gameInfo.genres">
				<button  v-for="genre in props.gameInfo.genres" 
				class="game_metadata_button"
				:key="genre"
				@click="() => handleMetadataClick('genres', [{ 
					title: genre, 
					value: genre 
				}])">
					{{ genre }}
				</button>
			</template>
			
			<template v-else>
				<SkeletonLoader/>
				<SkeletonLoader/>
			</template>
		</div>

		<div class="game_metadata game_metadata--date">
			Дата выхода: 
			<SkeletonLoader :is-loading="!date">
				<span class="game_metadata_value">{{ date }}</span>
			</SkeletonLoader>
		</div>

		<div class="game_metadata game_metadata--developer">
			Разработчик: 
			<SkeletonLoader :is-loading="!props.gameInfo.developer">
				<button class="game_metadata_button"
				@click="() => props.gameInfo.developer && handleMetadataClick('developers', [{ 
					title: props.gameInfo.developer, 
					value: props.gameInfo.developer 
				}])">
					{{ props.gameInfo.developer }}
				</button>
			</SkeletonLoader>
		</div>

		<div class="game_metadata game_metadata--publisher">
			Издатель:
			<SkeletonLoader :is-loading="!props.gameInfo.publisher">
				<button class="game_metadata_button"
				@click="() => props.gameInfo.publisher && handleMetadataClick('publishers', [{ 
					title: props.gameInfo.publisher, 
					value: props.gameInfo.publisher 
				}])">
					{{ props.gameInfo.publisher }}
				</button>
			</SkeletonLoader> 
		</div>

		<div class="game_metadata game_metadata--description">
			Описание:
			<DescriptionSection :description="props.gameInfo.description"/>
		</div>
	</section>
</template>

<style scoped>
.game_info {
	--fs_info_main: 1.5rem;
	--fs_subtitle: 1.2rem;

	display: flex;
	flex-direction: column;
	gap: 2rem;
}

.game_metadata {
	--h_skeleton_loader: var(--fs_info_main);

	display: flex;
	align-items: center;
	flex-wrap: wrap;
	column-gap: var(--fs_subtitle);
	row-gap: calc(var(--fs_subtitle) / 2);
	font-size: var(--fs_subtitle);
	color: var(--c_text__muted);
}

.game_metadata_button {
	padding: 0.5rem;
	background-color: var(--c_bg__surface);
	color: var(--c_secondary__accent);
	font-size: var(--fs_subtitle);
	cursor: pointer;
}

.game_metadata_value {
	color: var(--c_text);
}

.game_metadata--genre {
	--w_skeleton_loader: 10rem;
}
.game_metadata--date {
	--w_skeleton_loader: calc(var(--fs_info_main) * 16);
}
.game_metadata--developer,
.game_metadata--publisher {
	--w_skeleton_loader: calc(var(--fs_info_main) * 8);
}
.game_metadata--description {
	width: 75%;
}

@media (max-width: 600px) {
	.game_info {
		gap: 1rem;
	}

	.game_metadata--description {
		width: 100%;
	}
}
</style>