<script setup lang="ts">
import AuthForm from "@/widgets/auth/ui/AuthForm.vue"
import RegistartionFrom from "@/widgets/registration/ui/RegistartionFrom.vue"
import { ref } from "vue"

const isAuth = ref(true)

const handleSwitchForm = () => { isAuth.value = !isAuth.value }
</script>

<template>
	<div class="auth_page">
		<div class="forms_container" :class="{ forms_container__registration: !isAuth }">
			<section class="form" v-if="isAuth">
				<h2 class="title">Вход</h2>
				<AuthForm/>
			</section>

			<div class="form_switcher">
				{{ isAuth ? "Новенький? Тогда тебе сюда" : "Мы знакомы? Давай проверим"}}
				<button class="switch_button" 
				:class="{ switch_button__registration: !isAuth}" 
				@click="handleSwitchForm">
					{{ isAuth ? "Регистрация" :  "Вход"}}
				</button>
			</div>

			<section class="form" v-if="!isAuth">
				<h2 class="title">Регистрация</h2>
				<RegistartionFrom/>
			</section>
		</div>
	</div>
</template>

<style scoped>
.auth_page {
	display: flex;
	width: 100%;
	height: 100vh;
	background-color: var(--c_bg);
}

.forms_container {
	margin: auto;
	display: grid;
	grid-template-columns: repeat(2, 1fr);
	width: 55rem;
	min-height: 35rem;
	box-shadow:
		0 0 0.375rem var(--c_secondary__accent),
		0 0 0.75rem var(--c_secondary__accent),
		0 0 1.125rem var(--c_secondary__accent),
		0 0 1.5rem var(--c_secondary__accent),
		0 0 1.875rem rgba(102, 0, 153, 0.4);
}
.forms_container__registration {
	box-shadow:
		0 0 0.375rem var(--c_tertiary__accent),
		0 0 0.75rem var(--c_tertiary__accent),
		0 0 1.125rem var(--c_tertiary__accent),
		0 0 1.5rem var(--c_tertiary__accent),
		0 0 1.875rem rgba(204, 153, 0, 0.4);
}

.form {
	padding: 2.5rem;
	display: flex;
	flex-direction: column;
	align-items: center;
}

.title {
	margin-bottom: 1.75rem;
	font-size: 1.5rem;
	text-decoration: underline;
}

.form_switcher {
	padding: 2.5rem;
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	text-align: center;
	row-gap: 1rem;
	background-color: var(--c_bg__surface);
}

.switch_button {
	background-color: transparent;	
	color: var(--c_tertiary__accent);
	cursor: pointer;
}
.switch_button__registration {
	color: var(--c_secondary__accent);
}
</style>