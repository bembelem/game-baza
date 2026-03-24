<script setup lang="ts">
import FormField from "@/shared/ui/FormField.vue"
import InputField from "@/shared/ui/InputField.vue"
import PasswordField from "@/shared/ui/PasswordField.vue"
import SubmitButton from "@/shared/ui/SubmitButton.vue"
import { useForm } from "vee-validate"
import { usernameValidate, emailValidate, birthdayValidate, passwordValidate } from "@/features/registration/lib/registrationValidation"
import { computed } from "vue"
import { registrationFetch } from "@/features/registration/api/registrationAPI"

export interface RegistrationFormFields {
	username: string,
	email: string,
	birthday: string
	password: string,
} 

const { values, errors, meta, isSubmitting, handleSubmit, isFieldValid } = useForm<RegistrationFormFields>({
	validationSchema: {
		username: usernameValidate,
		email: emailValidate,
		birthday: birthdayValidate,
		password: passwordValidate
	}
})

const isFormFulfilled = computed(() => meta.value.touched && meta.value.valid)

const formatDate = (input: string) => {
	const digits = input.replace(/\D/g, "").slice(0, 8)

	if (digits.length <= 2) return digits
	if (digits.length <= 4) return `${digits.slice(0, 2)}.${digits.slice(2)}`
	return `${digits.slice(0, 2)}.${digits.slice(2, 4)}.${digits.slice(4)}`
}

const onSubmit = handleSubmit(async () => {
	try {
		console.log(values)
		const data = await registrationFetch(values)
		console.log(data)
	} catch (error) {
		console.log(error)
	}
})
</script>

<template>
	<form class="registration_form" @submit.prevent="onSubmit">
		<FormField
		label="Никнейм"
		:error="errors.username"
		:is-valid="isFieldValid('username')">
			<InputField 
			name="username"
			:max-length="20"
			auto-complete="username"/>
		</FormField>

		<FormField
		label="Логин"
		:error="errors.email"
		:is-valid="isFieldValid('email')">
			<InputField 
			name="email"
			auto-complete="email"/>
		</FormField>

		<FormField
		label="Дата рождения"
		:error="errors.birthday"
		:is-valid="isFieldValid('birthday')">
			<InputField
			name="birthday"
			placeholder="дд.мм.гггг"
			:max-length="10"
			:format-input="formatDate"/>
		</FormField>
		
		<FormField
		label="Пароль"
		:error="errors.password"
		:is-valid="isFieldValid('password')">
			<PasswordField 
			name="password"/>
		</FormField>

		<SubmitButton 
		label="зарегистрироваться"
		:is-available="isFormFulfilled"
		:is-submitting="isSubmitting"/>
	</form>
</template>

<style scoped>
.registration_form {
	--bc_input_field: var(--c_tertiary);
	--bc_input_field__focus: var(--c_tertiary__accent);
	--bc_password_field: var(--c_tertiary);
	--bc_password_field__focus: var(--c_tertiary__accent);
	--bc_submit_button: var(--c_tertiary);
	--bc_submit_button__accent: var(--c_tertiary__accent);

	display: flex;
	flex-direction: column;
	justify-content: center;
	width: 100%;
	flex: 1;
	row-gap: 1rem;
}
</style>