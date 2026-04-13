<script setup lang="ts">
import FormField from "@/shared/ui/FormField.vue"
import InputField from "@/shared/ui/InputField.vue"
import PasswordField from "@/shared/ui/PasswordField.vue"
import SubmitButton from "@/shared/ui/SubmitButton.vue"
import { type AuthResponseError, authFetch } from "@/features/auth/api/authAPI"
import { useRouter } from "vue-router"
import { ref, computed } from "vue"
import { useForm } from "vee-validate"
import { emailValidate, passwordValidate } from "../lib/authValidation"
import { authStore } from "@/entities/user/store/authStore"
import { isAPIValidationError } from "@/shared/interface/APIError"

export interface AuthFormFields {
	email: string,
	password: string
}

const router = useRouter()

const networkError = ref<string | null>(null)

const { values, errors, meta, isSubmitting, handleSubmit, isFieldValid, setErrors } = useForm<AuthFormFields>({
  	validationSchema: {
		email: emailValidate,
		password: passwordValidate
 	}, 
})

const isFormFulfilled = computed(() => meta.value.touched && meta.value.valid)

const onSubmit = handleSubmit(async () => {
	authStore.isPending.value = true
	networkError.value = null

	try {
		const data = await authFetch(values)
		authStore.data.value = data
		router.push("/games")
	} catch (error) {
		if (error instanceof TypeError) {
			networkError.value = "Не удалось подключиться к серверу. Проверьте интернет и попробуйте снова"
			return
		}

		if (isAPIValidationError(error)) {
			const { message, details } = error as AuthResponseError
			if (Object.keys(details).length) {
				setErrors(details)
			} else {
				networkError.value = message
			}
			return
		}

		console.error("Непредвиденная ошибка", error)
	} finally {
		authStore.isPending.value = false
	}
})
</script>

<template>
	<form class="auth_form" @submit.prevent="onSubmit">
		<FormField
		label="Email"
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
			{{ networkError }}
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