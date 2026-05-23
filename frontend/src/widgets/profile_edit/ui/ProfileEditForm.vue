<script lang="ts" setup>
import { ref, computed } from "vue"
import { useRouter } from "vue-router"
import { useForm } from "vee-validate"
import FormField from "@/shared/ui/FormField.vue"
import InputField from "@/shared/ui/InputField.vue"
import PasswordField from "@/shared/ui/PasswordField.vue"
import SubmitButton from "@/shared/ui/SubmitButton.vue"
import ConfirmDialog from "@/shared/ui/ConfirmDialog.vue"
import { profileEditFetch, profileDeleteFetch } from "@/features/profile_edit/api/profileEditAPI"
import { logoutFetch } from "@/features/auth/api/authAPI"
import { usernameValidate, emailValidate, birthdateValidate, passwordValidate } from "@/entities/user/lib/userValidation"
import { toProfileEditPayload } from "../lib/profileEditTransform"
import { authStore } from "@/entities/user/store/authStore"
import { isAPIValidationError } from "@/shared/interface/APIError"
import { Routes } from "@/shared/lib/router"
import { parseISOToDate, formatDateInput } from "@/shared/lib/date"
import { updateFetchDataController } from "@/shared/lib/fetchData"

export interface ProfileEditFormFields {
	username: string
	email: string
	birthdate: string
	newPassword: string
	confirmPassword: string
}

const router = useRouter()

const successMessage = ref<string | null>(null)
const errorMessage = ref<string | null>(null)
const isDeleteDialogVisible = ref(false)
const isDeletePending = ref(false)
const profileDeleteController = ref<AbortController>()

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

function handleLogout() {
	authStore.data.value = null
	router.push(Routes.auth)
	logoutFetch().catch(error => console.error("Непредвиденная ошибка", error))
}

async function handleProfileDelete() {
	const newGameInfoController = updateFetchDataController(profileDeleteController)
	isDeletePending.value = true

	try {
		await profileDeleteFetch(newGameInfoController)
		authStore.data.value = null
		router.push(Routes.auth)
	} catch (error) {
		if (error instanceof TypeError) {
			errorMessage.value = "Не удалось подключиться к серверу"
			return
		}
		errorMessage.value = "Не удалось удалить аккаунт"
		console.error("Непредвиденная ошибка", error)
	} finally {
		profileDeleteController.value = undefined
		isDeleteDialogVisible.value = false
		isDeletePending.value = false
	}
}

function handleCancelProfileDelete() {
	profileDeleteController.value?.abort()
	isDeleteDialogVisible.value = false
}
</script>

<template>
	<form
	class="edit_profile_form"
	@submit.prevent="onSubmit">
		<h1 class="greeting">Привет, {{ userName }}!</h1>

		<section class="section">
			<p class="section_label">ОСНОВНАЯ ИНФОРМАЦИЯ</p>

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
			<p class="section_label">СМЕНА ПАРОЛЯ</p>
			<p class="section_hint">Оставьте пустым, если не хотите менять пароль</p>

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
			<div class="footer_row">
				<div class="submit_button_container">
					<SubmitButton
					label="Сохранить изменения"
					:is-submitting="isSubmitting"/>
				</div>

				<p
				v-if="successMessage"
				class="footer_message footer_message--success">
					{{ successMessage }}
				</p>

				<p
				v-else-if="errorMessage"
				class="footer_message footer_message--error">
					{{ errorMessage }}
				</p>
			</div>

			<div class="footer_row">
				<button
				class="action_button action_button--logout"
				type="button"
				@click="handleLogout">
					Выйти
				</button>

				<button
				class="action_button action_button--delete"
				type="button"
				@click="isDeleteDialogVisible = true">
					Удалить аккаунт
				</button>
			</div>
		</div>
	</form>

	<ConfirmDialog
	class="delete_confirm_dialog"
	v-if="isDeleteDialogVisible"
	title="Удалить аккаунт?"
	message="Это действие необратимо. Все данные будут удалены."
	confirm-label="Удалить"
	:is-confirming="isDeletePending"
	@confirm="handleProfileDelete"
	@cancel="handleCancelProfileDelete"/>
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

.section_label {
	font-size: var(--fs__lg);
	color: var(--c_text__muted);
}

.section_hint {
	font-size: var(--fs__xs);
	color: var(--c_text__muted);
}

.divider {
	border: none;
	border-top: var(--border__md) solid var(--c_bg__accent);
}

.footer {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: var(--space__md);
	margin-top: var(--space__lg);
	width: 100%;
}

.footer_row {
	display: flex;
	align-items: center;
	flex-wrap: wrap;
	gap: var(--space__md);
	width: 100%;
}

.submit_button_container {
	width: 50%;
}

.footer_message {
	font-size: var(--fs__xs);
	text-align: center;
}
.footer_message--success {
	color: var(--c_text__success);
}
.footer_message--error {
	color: var(--c_text__error);
}

.action_button {
	background: none;
	border: none;
	padding: 0;
	cursor: pointer;
}
.action_button--logout {
	color: var(--c_text__muted);
}
.action_button--delete {
	color: var(--c_text__error);
}

.delete_confirm_dialog {
	--bc_submit_button: var(--c_error);
	--bc_submit_button__accent: var(--c_error_bright);
}

@media (max-width: 1024px) {
	.section {
		width: 75%;
	}
	.submit_button_container {
		width: 75%;
	}
}
@media (max-width: 600px) {
	.section {
		width: 100%;
	}
	.submit_button_container {
		width: 100%;
	}
	.footer_row {
		justify-content: space-evenly;
	}
}
</style>