<script setup lang="ts">
import { ref, onMounted } from "vue"
import { RouterView } from "vue-router"
import AppHeader from "@/widgets/header/ui/AppHeader.vue"
import LoadIndicator from "@/shared/ui/LoadIndicator.vue"
import { authStore } from "@/entities/user/store/authStore"
import { getUserFetch } from "@/entities/user/api/userAPI"
import { isAPIValidationError } from "@/shared/interface/APIError"

const isLoading = ref(false)

onMounted(async () => {
	authStore.isPending.value = true
	isLoading.value = true

	try {
		const data = await getUserFetch()
		authStore.data.value = data
	} catch (error) {
		if (error instanceof TypeError) {
			authStore.error.value = "Не удалось подключиться к серверу. Проверьте интернет и попробуйте снова"
			return
		}

		if (isAPIValidationError(error)) {
			authStore.error.value = error.message
			return
		}

		authStore.error.value = "Непредвиденная ошибка"
		console.error("Непредвиденная ошибка", error)
	} finally {
		authStore.isPending.value = false
		isLoading.value = false
	}
})
</script>

<template>
	<div
	v-if="isLoading"
	class="load_container">
		<LoadIndicator :is-short="false"/>
	</div>

	<template v-else>
		<AppHeader/>
		<div class="router_view">
			<RouterView/>
		</div>
	</template>
</template>

<style scoped>
.load_container {
	--fs_load: var(--fs__2xl);
	
  	margin: auto;
}

.router_view {
	margin-top: var(--h_header);
	padding: 0 var(--p_layout);;
}
</style>