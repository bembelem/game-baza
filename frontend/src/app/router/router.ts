import AuthPage from "@/pages/auth/ui/AuthPage.vue"
import GamesPage from "@/pages/games/ui/GamesPage.vue"
import GameInfoPage from "@/pages/game_info/ui/GameInfoPage.vue"
import { Routes } from "@/shared/lib/router"
import { createRouter, createWebHistory } from "vue-router"


const routes = [
	{ path: "/", redirect: "/games" },
	{ path: "/auth", name: Routes.auth, component: AuthPage },
	{ path: "/games", name: Routes.games, component: GamesPage },
	{ path: "/game_info", name: Routes.gameInfo, component: GameInfoPage }
]

export const router = createRouter({
  	history: createWebHistory(),
  	routes
})