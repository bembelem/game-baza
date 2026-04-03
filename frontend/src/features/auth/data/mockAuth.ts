import type { AuthResponse, AuthResponseError } from "../api/authAPI"


export const mockAuthResponse: AuthResponse = {
	access_token: "token",
  	token_type: "access_token"
}

export const mockAuthError: AuthResponseError = {
	details: {
		email: "Неверный адрес электронной почты",
		password: "Неверный пароль"
	}
}