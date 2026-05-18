<script lang="ts" setup>
import { ref } from "vue"

import AuthForm from "@/widgets/auth/ui/AuthForm.vue"
import RegistartionForm from "@/widgets/registration/ui/RegistartionForm.vue"

const isAuth = ref(true)

function handleSwitchForm() {
	isAuth.value = !isAuth.value
}
</script>

<template>
	<div class="auth_page">
		<div
		class="forms_container"
		:class="{ 'forms_container--registration': !isAuth }">
			<section
			v-if="isAuth"
			class="form">
				<h2 class="title">Вход</h2>
				<AuthForm />
			</section>

			<div class="form_switcher">
				{{ isAuth ? "Новенький? Тогда тебе сюда" : "Мы знакомы? Давай проверим" }}
				<button
				class="switch_button"
				:class="{ 'switch_button--registration': !isAuth }"
				@click="handleSwitchForm">
					{{ isAuth ? "Регистрация" : "Вход" }}
				</button>
			</div>

			<section
			v-if="!isAuth"
			class="form">
				<h2 class="title">Регистрация</h2>
				<RegistartionForm />
			</section>
		</div>
	</div>
</template>

<style scoped>
.auth_page {
	display: flex;
}

.forms_container {
	display: grid;
	grid-template-columns: repeat(2, 1fr);
	margin: auto;
	max-width: 80rem;
	box-shadow: var(--neon__purple);
}
.forms_container--registration {
	box-shadow: var(--neon__gold);
}

.form {
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: var(--space__xl);
	gap: var(--space__lg);
}

.title {
	font-size: var(--fs__xl);
	text-decoration: underline;
}

.form_switcher {
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	padding: var(--space__xl);
	gap: var(--space__sm);
	background-color: var(--c_bg__surface);
	text-align: center;
	text-wrap: balance;
}

.switch_button {
	background-color: transparent;
	color: var(--c_brand__gold_bright);
	cursor: pointer;
}
.switch_button--registration {
	color: var(--c_brand__purple_bright);
}

@media (max-width: 600px) {
	.auth_page {
		height: 100%;
	}

	.forms_container {
		display: grid;
		grid-template-columns: 1fr;
		grid-template-rows: auto 1fr;
		margin: 0;
		min-height: unset;
	}

	.form,
	.form_switcher {
		order: 1;
	}

	.form_switcher {
		order: 2;
		background-color: transparent;
	}
}
</style>