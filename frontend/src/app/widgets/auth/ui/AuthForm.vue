<script setup lang="ts">
import FormField from "@/shared/ui/FormField.vue"
import InputField from "@/shared/ui/InputField.vue"
</script>

<template>
	<form class="auth_form">
		<FormField
		label="Логин"
		error="Поле должно быть заполнено">
			<InputField/>
		</FormField>
		<FormField
		label="Пароль"
		error="Поле должно быть заполнено">
			<InputField
			type="password"/>
		</FormField>
	</form>
</template>

<style scoped>
.auth_form {
	display: flex;
	flex-direction: column;
	justify-content: center;
	width: 100%;
	flex: 1;
	row-gap: 1rem;
}
</style>