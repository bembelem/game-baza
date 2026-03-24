<script setup lang="ts">
import FormField from "@/shared/ui/FormField.vue"
import InputField from "@/shared/ui/InputField.vue"
import PasswordField from "@/shared/ui/PasswordField.vue"
import SubmitButton from "@/shared/ui/SubmitButton.vue"
import { useForm } from "vee-validate"
import { emailValidate, passwordValidate } from "@/features/auth/lib/authValidation"
import { computed } from "vue"
import { authFetch } from "@/features/auth/api/authAPI"

export interface AuthFormFields {
	email: string,
	password: string 
} 

const { values, errors, meta, isSubmitting, handleSubmit, isFieldValid } = useForm<AuthFormFields>({
  	validationSchema: {
		email: emailValidate,
		password: passwordValidate
 	}, 
})

const isFormFulfilled = computed(() => meta.value.touched && meta.value.valid)

const onSubmit = handleSubmit(async () => {
	try {
		console.log(values)
		const data = await authFetch(values)
		console.log(data)
	} catch (error) {
		console.log(error)
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
</style>