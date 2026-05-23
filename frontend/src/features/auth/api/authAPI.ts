import type { User } from "@/entities/user/model/User"
import type { APIValidationError } from "@/shared/interface/APIError"


export interface AuthPayload {
	email: string,
	password: string
}

export type AuthResponseError = APIValidationError<Partial<AuthPayload>>


export async function authFetch(authPayload: AuthPayload): Promise<User> {
	const response = await fetch("http://localhost:8000/auth/login", { 
		method: "POST",
		body: JSON.stringify(authPayload),
		headers: { "Content-Type": "application/json" },
		credentials: "include"
	})
	const data = await response.json()

	if (!response.ok) {
		throw data 
	}

	return data
}


export async function logoutFetch() {
	const response = await fetch("http://localhost:8000/auth/logout", {
		method: "POST",
		credentials: "include"
	})

	if (!response.ok) {
		throw new Error(`Ошибка logoutFetch: ${response.status}`)
	}
}