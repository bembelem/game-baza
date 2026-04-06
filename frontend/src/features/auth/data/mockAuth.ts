import type { AuthResponseError } from "../api/authAPI"


export const mockAuthError: AuthResponseError = {
	details: {
		email: "Неверный адрес электронной почты",
		password: "Неверный пароль"
	}
}