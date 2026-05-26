export function usernameValidate(value: string) {
	if (!value) 
		return "Никнейм обязателен"
	if (!/^[a-zA-Z0-9_ ]{3,50}$/.test(value))
    	return "От 3 до 50 символов: латиница, цифры, подчёркивания, пробелы"

	return true
}


export function emailValidate(value: string) {
	if (!value) 
		return "Логин обязателен"
	if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) 
		return "Введите корректный логин"

	return true
}

// accepts string instead of Date - UI compromise for masked input (dd.mm.yyyy)
export function birthdateValidate(value: string) {
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


export function passwordValidate(value: string) {
	if (!value) 
		return "Пароль обязателен"
	if (value.length < 6
    	|| value.length > 50
		|| !/^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};":"\\|,.<>\/?]+$/.test(value)
		|| !/[0-9]/.test(value)
		|| !/[!@#$%^&*()_+\-=\[\]{};":"\\|,.<>\/?]/.test(value) 
	) return "От 6 до 50 символов: латиница, хотя бы одна цифра и один спецсимвол"
	
	return true
}