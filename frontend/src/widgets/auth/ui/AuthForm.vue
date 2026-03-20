<script setup lang="ts">
import FormField from "@/shared/ui/FormField.vue"
import InputField from "@/shared/ui/InputField.vue"
import { useForm, useField } from "vee-validate"
import { emailValidate, passwordValidate } from "../lib/authValidation"
import { authFetch } from "@/features/auth/api/authAPI"


export interface AuthFormFields {
	email: string,
	password: string 
} 

const { values, isSubmitting, handleSubmit } = useForm<AuthFormFields>({
  	validationSchema: {
		email: emailValidate,
		password: passwordValidate
 	}, 
})

const fieldOptions = { validateOnValueUpdate: false }
const { value: emailValue, errorMessage: emailError } = useField('email', undefined, fieldOptions)
const { value: passwordValue, errorMessage: passwordError } = useField('password', undefined, fieldOptions)

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
		:error="emailError">
			<InputField 
			v-model="emailValue"/>
		</FormField>
		<FormField
		label="Пароль"
		:error="passwordError">
			<InputField 
			v-model="passwordValue"
			type="password"/>
		</FormField>

		<input class="submit_button" 
		type="submit"
		value="войти"
		:disabled="isSubmitting"/>
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

.submit_button {
	margin-top: 2rem;
	padding: 0.5rem;
	border: 0.25rem solid var(--c_secondary);
	background-color: var(--c_secondary);
}
.submit_button:disabled {
	border-color: var(--c_placeholder);
	background-color: transparent;
	color: var(--c_placeholder);
}
</style>