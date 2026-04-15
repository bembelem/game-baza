<script setup lang="ts">
import UserIcon from "@/assets/icons/user.svg?component"
import { computed } from "vue"
import { authStore } from "@/entities/user/store/authStore"
import { RouterLink, useRoute } from "vue-router"
import { Routes } from "@/shared/lib/router"

const route = useRoute()

const userRoute = computed(() => authStore.data.value ? "/user" : "/auth")
</script>

<template>
	<div class="header" :class="{ 'header--highlighted': route.name != Routes.auth }">
		<RouterLink to="/">
			<p class="logo"><span class="underlining"></span></p>
		</RouterLink>
		<div class="search_input"></div>
		<RouterLink :to="userRoute" v-if="route.name != Routes.auth">
			<UserIcon class="user_icon" :class="{ 'user_icon--active': authStore.data.value }"/>
		</RouterLink>
	</div>
</template>

<style scoped>
.header {
	z-index: 10;
	box-sizing: border-box;
	position: fixed;
	padding: 0 4rem;
	display: flex;
	align-items: center;
	column-gap: 1rem;
	width: 100%;
	height: var(--h_header);
  	background-color: rgba(11, 13, 23, 0.7);
	backdrop-filter: blur(4px);
  	-webkit-backdrop-filter: blur(4px); 
}
.header--highlighted {
	border-bottom: 0.125rem solid var(--c_secondary__accent);
	box-shadow:
		0 0 0.375rem var(--c_secondary__accent),
		0 0 0.75rem var(--c_secondary__accent),
		0 0 1.125rem var(--c_secondary__accent),
		0 0 1.5rem var(--c_secondary__accent),
		0 0 1.875rem rgba(102, 0, 153, 0.4);
}

.logo {
	font-size: 2rem;
	text-decoration: none;
	font-family: "Sixtyfour";
	color: var(--c_secondary__accent);
}
.logo::before {
	content: "GAMEBAZA";
}

.underlining::before {
	content: ">_";
	animation-name: blinking;
	animation-duration: 1s;
	animation-iteration-count: infinite;
}
@keyframes blinking {
	50% {
		opacity: 0;
	}
	100% {
		opacity: 1;
	}
}

.search_input {
	display: flex;
	flex: 1;
}

.user_icon {
	flex-shrink: 0;
	width: 3rem;
	height: 3rem;
	color: var(--c_placeholder);
}
.user_icon--active {
	color: var(--c_highlight__accent);
}

@media (max-width: 1024px) {
	.header {
		padding: 0 2rem;
	}
	.logo::before {
		content: "GB";
	}
}
@media (max-width: 600px) {
	.header {
		padding: 0 1rem;
	}
	.underlining::before {
		content: "";
	}
}
</style>