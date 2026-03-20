<script setup lang="ts">
import AuthForm from "@/widgets/auth/ui/AuthForm.vue"
</script>

<template>
	<div class="auth_page">
		<div class="forms_container">
			<section class="auth_form_container">
				<h2 class="title">Вход</h2>
				<AuthForm/>
			</section>

			<div class="form_switcher">
				<p>Новенький? Тогда тебе сюда</p>
				<button class="switch_button">Регистрация</button>
			</div>
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
		0 0 0.375rem var(--c_secondary),
		0 0 0.75rem var(--c_secondary),
		0 0 1.125rem var(--c_secondary),
		0 0 1.5rem var(--c_secondary),
		0 0 1.875rem rgba(102, 0, 153, 0.4);
}

.auth_form_container {
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
	color: var(--c_highlight__accent);
	cursor: pointer;
}
</style>