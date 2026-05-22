<script lang="ts" setup>
import { ref, computed } from "vue"
import { useRouter } from "vue-router"
import { useForm } from "vee-validate"
import FormField from "@/shared/ui/FormField.vue"
import InputField from "@/shared/ui/InputField.vue"
import PasswordField from "@/shared/ui/PasswordField.vue"
import SubmitButton from "@/shared/ui/SubmitButton.vue"
import { type RegistrationResponseError, registrationFetch } from "@/features/registration/api/registrationAPI"
import { usernameValidate, emailValidate, birthdateValidate, passwordValidate } from "@/entities/user/lib/userValidation"
import { toRegistrationPayload } from "../lib/registrationTransform"
import { authStore } from "@/entities/user/store/authStore"
import { isAPIValidationError } from "@/shared/interface/APIError"
import { Routes } from "@/shared/lib/router"
import { formatDateInput } from "@/shared/lib/date"

export interface RegistrationFormFields {
	username: string
	email: string
	birthdate: string
	password: string
}

const router = useRouter()

const networkError = ref<string | null>(null)

const { values, errors, meta, isSubmitting, handleSubmit, isFieldValid, setErrors } = useForm<RegistrationFormFields>({
	validationSchema: {
		username: usernameValidate,
		email: emailValidate,
		birthdate: birthdateValidate,
		password: passwordValidate,
	},
})

const isFormFulfilled = computed(() => meta.value.touched && meta.value.valid)

const onSubmit = handleSubmit(async () => {
	authStore.isPending.value = true
	networkError.value = null

	try {
		const transformedValues = toRegistrationPayload({ ...values })
		const data = await registrationFetch(transformedValues)
		authStore.data.value = data
		router.push(Routes.games)
	} catch (error) {
		if (error instanceof TypeError) {
			networkError.value = "Не удалось подключиться к серверу. Проверьте интернет и попробуйте снова"
			return
		}

		if (isAPIValidationError(error)) {
			const { message, details } = error as RegistrationResponseError
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
	<form
	class="registration_form"
	@submit.prevent="onSubmit">
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
		label="Email"
		:error="errors.email"
		:is-valid="isFieldValid('email')">
			<InputField
			name="email"
			auto-complete="email"/>
		</FormField>

		<FormField
		label="Дата рождения"
		:error="errors.birthdate"
		:is-valid="isFieldValid('birthdate')">
			<InputField
			name="birthdate"
			placeholder="дд.мм.гггг"
			:max-length="10"
			:format-input="formatDateInput"/>
		</FormField>

		<FormField
		label="Пароль"
		:error="errors.password"
		:is-valid="isFieldValid('password')">
			<PasswordField name="password"/>
		</FormField>

		<p
		v-if="networkError"
		class="network_error">
			{{ networkError }}
		</p>

		<SubmitButton
		label="зарегистрироваться"
		:is-available="isFormFulfilled"
		:is-submitting="isSubmitting"/>
	</form>
</template>

<style scoped>
.registration_form {
	--bc_input_field: var(--c_brand__gold);
	--bc_input_field__focus: var(--c_brand__gold_bright);
	--bc_password_field: var(--c_brand__gold);
	--bc_password_field__focus: var(--c_brand__gold_bright);
	--bc_submit_button: var(--c_brand__gold);
	--bc_submit_button__accent: var(--c_brand__gold_bright);

	display: flex;
	flex-direction: column;
	justify-content: center;
	gap: var(--space__sm);
}
</style>