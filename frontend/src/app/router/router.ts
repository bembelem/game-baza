import AuthPage from "@/pages/auth/ui/AuthPage.vue"
import { Routes } from "@/shared/lib/router"
import { createRouter, createWebHistory } from "vue-router"


const routes = [
	{ path: "/", redirect: "/auth" },
	{ path: "/auth", name: Routes.auth, component: () => AuthPage }
]

export const router = createRouter({
  	history: createWebHistory(),
  	routes
})