import AuthPage from "@/pages/auth/ui/AuthPage.vue"
import GamesPage from "@/pages/games/ui/GamesPage.vue"
import { Routes } from "@/shared/lib/router"
import { createRouter, createWebHistory } from "vue-router"


const routes = [
	{ path: "/", redirect: "/games" },
	{ path: "/auth", name: Routes.auth, component: () => AuthPage },
	{ path: "/games", name: Routes.games, component: GamesPage }
]

export const router = createRouter({
  	history: createWebHistory(),
  	routes
})