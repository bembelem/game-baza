import type { User } from "@/entities/user/model/User"


export interface AuthPayload {
	email: string,
	password: string
}

export interface AuthResponseError {
	details: Partial<Record<keyof AuthPayload, string>>
}


export function isAuthResponseError(error: unknown): error is AuthResponseError {
	return error != null
		&& typeof error == "object"
		&& "details" in error
}


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
