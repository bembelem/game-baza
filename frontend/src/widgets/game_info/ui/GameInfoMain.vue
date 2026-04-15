<script setup lang="ts">
import SkeletonLoader from "@/shared/ui/SkeletonLoader.vue"
import type { GameBase } from "@/entities/game/model/Game"

const props = defineProps<{
	gameInfo?: GameBase
}>()
</script>


<template>
	<div class="game_info_main">
		<div class="image_container" :class="{ 
		'image_container--loaded': props.gameInfo?.image_url, 
		'image_container--skeleton': !props.gameInfo?.image_url }">
			<img class="image" 
			:src="props.gameInfo.image_url"
			alt="обложка игры"
			v-if="props.gameInfo">
		</div>
			
		<div class="info-main">
			<h1 v-if="props.gameInfo">{{ props.gameInfo.title }}</h1>
			
			<template v-else>
				<SkeletonLoader/>
				<SkeletonLoader class="skeleton_loader"/>	
			</template>

			<div class="min_price_container">
				<p v-if="props.gameInfo?.min_price_discount == 0">бесплатно</p>

				<p v-else>
					от
					<span class="min_price">
						<SkeletonLoader :is-loading="!props.gameInfo">
							{{ props.gameInfo?.min_price_discount }}
						</SkeletonLoader>
						<span :class="{ currency: !props.gameInfo }">₽</span>
					</span>
				</p>
			</div>

			<button class="button_scroll">
				Смотреть предложения ↓
			</button>
		</div>
	</div>
</template>

<style scoped>
.game_info_main {
	display: grid;
	grid-template-columns: repeat(2, 1fr);
	gap: 2rem;
}

.image_container {
	position: relative;
	aspect-ratio: 2.14 / 1;
	border: 0.25rem solid var(--c_bg__surface);
	transition: border-color 2s ease-in-out,
				box-shadow 2s ease-in-out;
}

.image_container::before {
	content: "";
	position: absolute;
	inset: 0;
	background: linear-gradient(
		135deg,
		transparent 0%,
		rgba(255, 255, 255, 0.05) 40%,
		rgba(255, 255, 255, 0.14) 50%,
		rgba(255, 255, 255, 0.05) 60%,
		transparent 100%
	);
	background-size: 400% 400%;
	background-repeat: no-repeat;
	filter: blur(20px);
	animation: image_skeleton 4s ease-in-out infinite;
	transition: opacity 0.2s ease-in-out;
}
@keyframes image_skeleton {
	0% {
		background-position: 180% 180%;
	}
	100% {
		background-position: -80% -80%;
	}
}

.image_container--skeleton {
	animation: border_skeleton 1s ease-in-out infinite;
}
.image_container.image_container--skeleton::before {
	opacity: 0;
}
.image_container--loaded {
	border-color: var(--c_highlight__accent);
	box-shadow:
		0 0 0.375rem var(--c_highlight__accent),
		0 0 0.75rem var(--c_highlight__accent),
		0 0 1.125rem var(--c_highlight__accent),
		0 0 1.5rem var(--c_highlight__accent),
		0 0 1.875rem rgba(255, 221, 0, 0.4);
}
@keyframes border_skeleton {
	50% {
		border-color: var(--c_bg__accent);
	}
	100% {
		border-color: var(--c_bg__surface);
	}
}

.image {
	width: 100%;
	height: 100%;
	object-fit: cover;
	object-position: center;
}

.info-main {
	--h_skeleton_loader: var(--fs_info_main);

	display: flex;
	flex-direction: column;
	row-gap: var(--fs_info_main);
	text-wrap: wrap;
	font-size: var(--fs_info_main);
}

.skeleton_loader {
	--w_skeleton_loader: 50%;
}

.min_price_container {
	margin-top: calc(var(--fs_info_main) / 2);
	font-size: calc(var(--fs_info_main) - 0.2rem);
}

.min_price {
	--w_skeleton_loader: calc(var(--fs_info_main) * 3);

	display: inline-flex;
	gap: 0.5rem;
	font-size: var(--fs_info_main);
}

.currency {
	animation: min_price_skeleton 0.5s ease-out infinite;
}
@keyframes min_price_skeleton {
	50% {
		transform: translateY(-80%);
	}
	100% {
		transform: translateY(0%);
	}
}

.button_scroll {
	padding: 0.5rem;
	width: fit-content;
	background-color: var(--c_highlight__accent);
	font-size: var(--fs_subtitle);
	transition: color 0.1s ease-out;
}

.button_scroll:active {
	color: var(--c_text);
}

@media (max-width: 600px) {
	.game_info_main {
		grid-template-columns: 1fr;
		gap: 1rem;
	}

	.button_scroll {
		width: 100%;
	}
}
</style>