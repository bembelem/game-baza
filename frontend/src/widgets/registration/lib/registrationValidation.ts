import type { RegistrationFormFields } from "../ui/RegistartionForm.vue"


export function usernameValidate(value: RegistrationFormFields["username"]) {
	if (!value) 
		return "Никнейм обязателен"
  	if (value.length < 3) 
		return "Минимум 3 символа"
	if (!/^[a-zA-Z0-9]+$/.test(value)) 
		return "Только латиница и цифры"

	return true
}


export function emailValidate(value: RegistrationFormFields["email"]) {
	if (!value) 
		return "Логин обязателен"
	if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) 
		return "Введите корректный логин"

	return true
}


export function birthdateValidate(value: RegistrationFormFields["birthdate"]) {
	if (!value) 
		return "День рождения обязателен"
	if (value.length < 10) 
		return "Введите полную дату"
	
  	const [day, month, year] = value.split(".").map(Number) as [number, number, number]
	const birthday = new Date(year, month -1, day)

	if (birthday.getFullYear() !== year 
		|| birthday.getMonth() !== month - 1 
		|| birthday.getDate() !== day
	) return "Несуществующая дата"

	if (birthday > new Date()) 
		return "Дата не может быть в будущем"

	return true
}


export function passwordValidate(value: RegistrationFormFields["password"]) {
	if (!value) 
		return "Пароль обязателен"
	if (value.length < 6) 
		return "Минимум 6 символов"
	if (!/^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};":"\\|,.<>\/?]+$/.test(value)) 
		return "Только латиница, цифры и спецсимволы"
	if (!/[0-9]/.test(value)) 
		return "Минимум одна цифра"
	if (!/[!@#$%^&*()_+\-=\[\]{};":"\\|,.<>\/?]/.test(value)) 
		return "Минимум один спецсимвол"
	
	return true
}