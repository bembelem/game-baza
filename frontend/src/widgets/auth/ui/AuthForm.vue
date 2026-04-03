<script setup lang="ts">
import FormField from "@/shared/ui/FormField.vue"
import InputField from "@/shared/ui/InputField.vue"
import PasswordField from "@/shared/ui/PasswordField.vue"
import SubmitButton from "@/shared/ui/SubmitButton.vue"
import { ref, computed } from "vue"
import { useForm } from "vee-validate"
import { emailValidate, passwordValidate } from "../lib/authValidation"
import { authFetch, isAuthResponseError } from "@/features/auth/api/authAPI"


export interface AuthFormFields {
	email: string,
	password: string
}

const networkError = ref(false)

const { values, errors, meta, isSubmitting, handleSubmit, isFieldValid, setErrors } = useForm<AuthFormFields>({
  	validationSchema: {
		email: emailValidate,
		password: passwordValidate
 	}, 
})

const isFormFulfilled = computed(() => meta.value.touched && meta.value.valid)

const onSubmit = handleSubmit(async () => {
	networkError.value = false

	try {
		const data = await authFetch(values)
		console.log(data)
	} catch (error) {
		if (error instanceof TypeError) {
			networkError.value = true
			return
		}

		if (isAuthResponseError(error)) {
			const { details } = error
			setErrors(details)
		}

		console.error("Непредвиденная ошибка", error)
	}
})
</script>

<template>
	<form class="auth_form" @submit.prevent="onSubmit">
		<FormField
		label="Логин"
		:error="errors.email"
		:is-valid="isFieldValid('email')">
			<InputField 
			name="email"
			auto-complete="email"/>
		</FormField>
		
		<FormField
		label="Пароль"
		:error="errors.password"
		:is-valid="isFieldValid('password')">
			<PasswordField 
			name="password"
			auto-complete="current-password"/>
		</FormField>

		<p class="network_error" v-if="networkError">
			Не удалось подключиться к серверу. Проверьте интернет и попробуйте снова
		</p>

		<SubmitButton
		label="вход"
		:is-available="isFormFulfilled"
		:is-submitting="isSubmitting"/>
	</form>
</template>

<style scoped>
.auth_form {
	--bc_input_field__focus: var(--c_secondary__accent);
	--bc_password_field__focus: var(--c_secondary__accent);

	display: flex;
	flex-direction: column;
	justify-content: center;
	width: 100%;
	flex: 1;
	row-gap: 1rem;
}

.network_error {
	text-align: center;
	text-wrap: balance;
	font-size: 0.75rem;
	color: var(--c_text__error);
}
</style>