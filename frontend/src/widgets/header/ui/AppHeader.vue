<script setup lang="ts">
import { RouterLink, useRoute } from "vue-router"
import { Routes } from "@/shared/lib/router"

const route = useRoute()
</script>

<template>
	<div class="header" :class="{ 'header--highlighted': route.name != Routes.auth }">
		<RouterLink to="/">
			<p class="logo"><span class="underlining"></span></p>
		</RouterLink>
	</div>
</template>

<style scoped>
.header {
	position: fixed;
	padding: 0 2rem;
	display: grid;
	grid-template-columns: 2fr 3fr 2fr;
	column-gap: 1rem;
	width: 100%;
	height: var(--h_header);
	place-items: center;
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

@media (max-width: 1024px) {
	.header {
		grid-template-columns: 1fr 5fr 1fr;
	}
	.logo::before {
		content: "GB";
	}
}
@media (max-width: 600px) {
	.header {
		grid-template-columns: 1fr 6fr;
	}
	.underlining::before {
		content: "";
	}
}
</style>