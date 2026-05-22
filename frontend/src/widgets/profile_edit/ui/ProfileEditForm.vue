<script lang="ts" setup>
import { ref, computed } from "vue"
import { useForm } from "vee-validate"
import FormField from "@/shared/ui/FormField.vue"
import InputField from "@/shared/ui/InputField.vue"
import PasswordField from "@/shared/ui/PasswordField.vue"
import SubmitButton from "@/shared/ui/SubmitButton.vue"
import { usernameValidate, emailValidate, birthdateValidate, passwordValidate } from "@/entities/user/lib/userValidation"
import { authStore } from "@/entities/user/store/authStore"
import { parseISOToDate } from "@/shared/lib/date"
import { toProfileEditPayload } from "../lib/profileEditTransform"
import { profileEditFetch } from "@/features/profile_edit/api/profileEditAPI"
import { formatDateInput } from "@/shared/lib/date"
import { isAPIValidationError } from "@/shared/interface/APIError"

export interface ProfileEditFormFields {
	username: string
	email: string
	birthdate: string
	newPassword: string
	confirmPassword: string
}

function newPasswordValidate(value: ProfileEditFormFields["newPassword"]) {
	if (!value) 
		return true

	return passwordValidate(value)
}

function confirmPasswordValidate(value: ProfileEditFormFields["confirmPassword"]) {
	if (!value && !values.newPassword) 
		return true
	if (!value) 
		return "Подтвердите пароль"
	if (value !== values.newPassword) 
		return "Пароли не совпадают"

	return true
}

const successMessage = ref<string | null>(null)
const errorMessage = ref<string | null>(null)

const { values, errors, isSubmitting, handleSubmit, isFieldValid } = useForm<ProfileEditFormFields>({
	validationSchema: {
		username: usernameValidate,
		email: emailValidate,
		birthdate: birthdateValidate,
		newPassword: newPasswordValidate,
		confirmPassword: confirmPasswordValidate,
	},
	initialValues: {
		username: authStore.data.value?.username ?? "",
		email: authStore.data.value?.email ?? "",
		birthdate: parseISOToDate(authStore.data.value?.birthdate ?? ""),
		newPassword: "",
		confirmPassword: "",
	},
})

const userName = computed(() => authStore.data.value?.username ?? "")

const onSubmit = handleSubmit(async (values) => {
	successMessage.value = null
	errorMessage.value = null

	try {
		const transformedValues = toProfileEditPayload({ ...values })
		const data = await profileEditFetch(transformedValues)
		authStore.data.value = data
		successMessage.value = "Данные успешно обновлены"
	} catch (error) {
		if (error instanceof TypeError) {
			errorMessage.value = "Не удалось подключиться к серверу"
			return
		}

		if (isAPIValidationError(error)) {
			errorMessage.value = error.message
			return
		}

		errorMessage.value = "Не удалось сохранить данные"
		console.error("Непредвиденная ошибка", error)
	}
})
</script>

<template>
	<form
	class="edit_profile_form"
	@submit.prevent="onSubmit">
		<h1 class="greeting">Привет, {{ userName }}!</h1>

		<section class="section">
			<p class="section__label">ОСНОВНАЯ ИНФОРМАЦИЯ</p>

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
		</section>

		<hr class="divider"/>

		<section class="section">
			<p class="section__label">СМЕНА ПАРОЛЯ</p>
			<p class="section__hint">Оставьте пустым, если не хотите менять пароль</p>

			<FormField
			label="Новый пароль"
			:error="errors.newPassword"
			:is-valid="isFieldValid('newPassword')">
				<PasswordField
				name="newPassword"
				auto-complete="new-password"/>
			</FormField>

			<FormField
			label="Подтвердите пароль"
			:error="errors.confirmPassword"
			:is-valid="isFieldValid('confirmPassword')">
				<PasswordField
				name="confirmPassword"
				auto-complete="new-password"/>
			</FormField>
		</section>

		<hr class="divider"/>

		<div class="footer">
			<div class="submit_button_container">
				<SubmitButton
				label="Сохранить изменения"
				:is-available="true"
				:is-submitting="isSubmitting"/>
			</div>

			<p
			v-if="successMessage"
			class="footer__message footer__message--success">
				{{ successMessage }}
			</p>

			<p
			v-else-if="errorMessage"
			class="footer__message footer__message--error">
				{{ errorMessage }}
			</p>
		</div>
	</form>
</template>

<style scoped>
.edit_profile_form {
	--bc_input_field: var(--c_brand__gold);
	--bc_input_field__focus: var(--c_brand__gold_bright);
	--bc_password_field: var(--c_brand__gold);
	--bc_password_field__focus: var(--c_brand__gold_bright);
	--bc_submit_button: var(--c_brand__gold);
	--bc_submit_button__accent: var(--c_brand__gold_bright);

	display: flex;
	flex-direction: column;
	gap: var(--space__sm);
}

.greeting {
	font-size: var(--fs__2xl);
	margin-bottom: var(--space__lg);
	overflow: hidden;
	text-overflow: ellipsis;
	white-space: nowrap;
}

.section {
	display: flex;
	flex-direction: column;
	gap: var(--space__sm);
	width: 50%;
}

.section__label {
	font-size: var(--fs__lg);
	color: var(--c_text__muted);
}

.section__hint {
	font-size: var(--fs__xs);
	color: var(--c_text__muted);
}

.divider {
	border: none;
	border-top: var(--border__md) solid var(--c_bg__accent) ;
}

.footer {
	display: flex;
	align-items: center;
	flex-wrap: wrap;
	gap: var(--space__md);
	width: 100%;
}

.submit_button_container {
	width: 25%;
}

.footer__message {
	font-size: var(--fs__sm);
}
.footer__message--success {
	color: var(--c_text__success);
}
.footer__message--error {
	color: var(--c_text__error);
}


@media (max-width: 1024px) {
	.section {
		width: 75%;
	}
	.submit_button_container {
		width: 50%;
	}
}
@media (max-width: 600px) {
	.section {
		width: 100%;
	}
	.submit_button_container {
		width: 100%;
	}
}
</style>