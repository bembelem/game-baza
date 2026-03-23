<script setup lang="ts">
import FormField from "@/shared/ui/FormField.vue"
import InputField from "@/shared/ui/InputField.vue"
import PasswordField from "@/shared/ui/PasswordField.vue"
import LoadIndicator from "@/shared/ui/LoadIndicator.vue"
import { useForm, useField } from "vee-validate"

export interface RegistrationFormFields {
	userName: string,
	email: string,
	birthday: string
	password: string,
} 

const { isSubmitting } = useForm<RegistrationFormFields>()

const useFormField = (name: string) => useField<string>(name, undefined, { validateOnValueUpdate: false })

const { value: userNameValue, errorMessage: userNameError } = useFormField('userName')
const { value: emailValue, errorMessage: emailError } = useFormField('email')
const { value: birthdayValue, errorMessage: birthdayError } = useFormField('birthday')
const { value: passwordValue, errorMessage: passwordError } = useFormField('password')

const formatDate = (input: string) => {
	const digits = input.replace(/\D/g, '').slice(0, 8)

	if (digits.length <= 2) return digits
	if (digits.length <= 4) return `${digits.slice(0, 2)}.${digits.slice(2)}`
	return `${digits.slice(0, 2)}.${digits.slice(2, 4)}.${digits.slice(4)}`
}
</script>

<template>
	<form class="auth_form">
		<FormField
		label="Никнейм"
		:error="userNameError">
			<InputField v-model="userNameValue"/>
		</FormField>
		<FormField
		label="Логин"
		:error="emailError">
			<InputField 
			v-model="emailValue"
			type="email"/>
		</FormField>
		<FormField
		label="Дата рождения"
		:error="birthdayError">
			<InputField
			placeholder="дд.мм.гггг"
			:format-input="formatDate"
			:max-length="10"
			v-model="birthdayValue"/>
		</FormField>
		<FormField
		label="Пароль"
		:error="passwordError">
			<PasswordField 
			v-model="passwordValue"/>
		</FormField>

		<button class="submit_button" 
		type="submit"
		:disabled="isSubmitting">
			<LoadIndicator class="load" :is-short="true" v-if="isSubmitting"/>
			<p v-else>зарегистрироваться</p>
		</button>
	</form>
</template>

<style scoped>
.auth_form {
	--bc_input_field: var(--c_highlight);
	--bc_input_field__focus: var(--c_highlight__accent);
	--bc_password_field: var(--c_highlight);
	--bc_password_field__focus: var(--c_highlight__accent);

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
	border: 0.25rem solid var(--c_highlight);
	background-color: var(--c_highlight);
	transition: background-color 0.2s ease-in-out,
				border-color 0.2s ease-in-out;
}
.submit_button:hover {
	border: 0.25rem solid var(--c_highlight__accent);
	background-color: var(--c_highlight__accent);
}
.submit_button:disabled {
	border-color: var(--c_placeholder);
	background-color: transparent;
	color: var(--c_placeholder);
}

.load {
	--fs_load: 1rem;
  	--c_load: var(--c_placeholder);
	--c_load__accent: var(--c_placeholder);
}
</style>