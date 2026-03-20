import type { AuthFormFields } from "../ui/AuthForm.vue"


export function emailValidate(value: AuthFormFields["email"]) {
	if (!value) return "Логин обязателен"
	if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) return "Введите корректный логин"

	return true
}


export function passwordValidate(value: AuthFormFields["password"]) {
	if (!value) return "Пароль обязателен"
	
	return true
}