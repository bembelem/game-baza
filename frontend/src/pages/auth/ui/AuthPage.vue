<script setup lang="ts">
import AuthForm from "@/widgets/auth/ui/AuthForm.vue"
import RegistartionForm from "@/widgets/registration/ui/RegistartionForm.vue"
import { ref } from "vue"

const isAuth = ref(true)

const handleSwitchForm = () => { isAuth.value = !isAuth.value }
</script>

<template>
	<div class="auth_page">
		<div class="forms_container" :class="{ 'forms_container--registration': !isAuth }">
			<section class="form" v-if="isAuth">
				<h2 class="title">Вход</h2>
				<AuthForm/>
			</section>

			<div class="form_switcher">
				{{ isAuth ? "Новенький? Тогда тебе сюда" : "Мы знакомы? Давай проверим"}}
				<button class="switch_button" 
				:class="{ 'switch_button--registration': !isAuth}" 
				@click="handleSwitchForm">
					{{ isAuth ? "Регистрация" :  "Вход"}}
				</button>
			</div>

			<section class="form" v-if="!isAuth">
				<h2 class="title">Регистрация</h2>
				<RegistartionForm/>
			</section>
		</div>
	</div>
</template>

<style scoped>
.auth_page {
	display: flex;
	width: 100%;
}

.forms_container {
	margin: auto;
	display: grid;
	grid-template-columns: repeat(2, 1fr);
	max-width: 55rem;
	width: 100%;
	min-height: 35rem;
	box-shadow:
		0 0 0.375rem var(--c_secondary__accent),
		0 0 0.75rem var(--c_secondary__accent),
		0 0 1.125rem var(--c_secondary__accent),
		0 0 1.5rem var(--c_secondary__accent),
		0 0 1.875rem rgba(102, 0, 153, 0.4);
}
.forms_container--registration {
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
	text-wrap: balance;
	row-gap: 1rem;
	background-color: var(--c_bg__surface);
}

.switch_button {
	background-color: transparent;	
	color: var(--c_tertiary__accent);
	cursor: pointer;
}
.switch_button--registration {
	color: var(--c_secondary__accent);
}

@media (max-width: 1024px) {
	.auth_page {
		padding: 2rem;
	}
	.forms_container {
		width: 100%;
	}
}
@media (max-width: 600px) {
	.auth_page {
		margin-top: var(--h_header);
		padding: 0;
	}
	.forms_container {
		margin: 0;
		padding: 1rem;
		grid-template-columns: 1fr;
		grid-template-rows: auto 1fr;
		row-gap: 2rem;
		min-height: unset;
	}
	.form,
	.form_switcher {
		padding: 0;
	}
	.form_switcher {
		order: 2;
		background-color: transparent;
	}
}
</style>