<script setup lang="ts">
import { ref, computed } from "vue"
import { useRouter, useRoute, RouterLink } from "vue-router"
import SearchBar from "@/shared/ui/SearchBar.vue"
import UserIcon from "@/assets/icons/user.svg?component"
import { useSearchGamesStore } from "@/features/search_games/store/searchGamesStore"
import { Routes } from "@/shared/lib/router"
import { authStore } from "@/entities/user/store/authStore"

const route = useRoute()
const router = useRouter()

const { searchGames, resetGames } = useSearchGamesStore()

const searchInput = ref("")

const isAuthRoute = computed(() => route.name != Routes.auth)
const userRoute = computed(() => authStore.data.value ? Routes.user : Routes.auth)

async function handleSearch() {
	if (!searchInput.value) return

	resetGames()
	searchGames({ title: [searchInput.value] })

	if (route.name != Routes.games) router.back()
}
</script>

<template>
	<div
	class="header"
	:class="{ 'header--highlighted': isAuthRoute }">
		<RouterLink to="/">
			<p class="logo"><span class="underlining"></span></p>
		</RouterLink>

		<SearchBar
		v-if="isAuthRoute"
		v-model="searchInput"
		placeholder="Игра..."
		@search="handleSearch"/>

		<RouterLink
		v-if="isAuthRoute"
		class="user_link"
		:to="userRoute">
			<UserIcon
			class="user_icon"
			:class="{ 'user_icon--active': authStore.data.value }"/>
		</RouterLink>
	</div>
</template>

<style scoped>
.header {
	z-index: 100;
	position: fixed;
	top: 0;
	display: grid;
	grid-template-columns: 1fr minmax(auto, 40rem) 1fr;
	align-items: center;
	gap: var(--space__md);
	width: 100%;
	height: var(--h_header);
	padding: 0 var(--p_layout);
	background-color: rgba(11, 13, 23, 0.7);
	backdrop-filter: blur(4px);
	-webkit-backdrop-filter: blur(4px);
}
.header--highlighted {
	border-bottom: var(--border__sm) solid var(--c_brand__purple_bright);
	box-shadow: var(--neon__purple);
}

.logo {
	font-family: var(--ff_brand);
	font-size: var(--fs__2xl);
	color: var(--c_brand__purple_bright);
	text-decoration: none;
}
.logo::before {
	content: "GAMEBAZA";
}

.underlining::before {
	content: ">_";
	animation: blinking 1s infinite;
}
@keyframes blinking {
	50% { 
		opacity: 0; 
	}
  	100% { 
		opacity: 1; 
	}
}

.user_link {
  	justify-self: end;
	min-width: max-content;
}

.user_icon {
	justify-self: end;
	width: var(--fs__3xl);
	height: var(--fs__3xl);
	color: var(--c_text__muted);
}
.user_icon--active {
  	color: var(--c_brand__gold_bright);
}

@media (max-width: 1024px) {
	.logo::before {
		content: "GB";
	}
}

@media (max-width: 600px) {
	.underlining::before {
		content: "";
	}
}
</style>