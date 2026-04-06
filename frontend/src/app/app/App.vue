<script setup lang="ts">
import LoadIndicator from "@/shared/ui/LoadIndicator.vue"
import AppHeader from "@/widgets/header/ui/AppHeader.vue"
import { RouterView } from "vue-router"
import { ref } from "vue"
import { onMounted } from "vue"
import { authStore } from "@/entities/user/store/authStore"
import { getUserFetch } from "@/entities/user/api/userAPI"
import "../styles/fonts.css"
import "../styles/main.css"
import "../styles/reset.css"

const isLoading = ref(false)

onMounted(async () => {
	authStore.isPending.value = true
	isLoading.value = true

	try {
		const data = await getUserFetch() 
		authStore.data.value = data
	} catch (error) {
		// TODO: обработать ошибку
		authStore.error.value = error instanceof Error ? error.message : String(error)
	} finally {
		authStore.isPending.value = false
		isLoading.value = false
	}
})
</script>

<template>
	<div class="load_container" v-if="isLoading">
		<LoadIndicator :is-short="false" />
	</div>
	<template v-else>
		<AppHeader/>
		<RouterView/>
	</template>
</template>

<style scoped>
.load_container {
	margin: auto;
}
</style>