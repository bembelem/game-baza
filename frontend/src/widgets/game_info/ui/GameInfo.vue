<script setup lang="ts">
import GameInfoMain from "./GameInfoMain.vue"
import SkeletonLoader from "@/shared/ui/SkeletonLoader.vue"
import DescriptionSection from "@/shared/ui/DescriptionSection.vue"
import { computed } from "vue"
import { mockGameInfo } from "@/entities/game/data/mockGames"

const date = computed(() => {
	if (!mockGameInfo.release_date) return

	const date = new Date(mockGameInfo.release_date)
  
	const options: Intl.DateTimeFormatOptions = {
		day: "numeric",
		month: "long",
		year: "numeric"
	}
	
	return date.toLocaleDateString("ru-RU", options)
})
</script>

<template>
	<section class="game_info">
		<GameInfoMain :game-info="mockGameInfo"/>

		<div class="game_metadata game_metadata--genre">
			Жанр:
			<template v-if="mockGameInfo.genres">
				<button class="game_metadata_button" v-for="genre in mockGameInfo.genres" :key="genre">
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
			<SkeletonLoader :is-loading="!mockGameInfo.developer">
				<button class="game_metadata_button">
					{{ mockGameInfo.developer }}
				</button>
			</SkeletonLoader>
		</div>

		<div class="game_metadata game_metadata--publisher">
			Издатель:
			<SkeletonLoader :is-loading="!mockGameInfo.publisher">
				<button class="game_metadata_button">
					{{ mockGameInfo.publisher }}
				</button>
			</SkeletonLoader> 
		</div>

		<div class="game_metadata game_metadata--description">
			Описание:
			<DescriptionSection :description="mockGameInfo.description"/>
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