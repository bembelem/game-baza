import type { User } from "@/entities/user/model/User"


export interface RegistrationPayload {
	username: string,
	email: string,
	password: string,
	birthdate: string
}

export interface RegistrationResponseError {
	details: Partial<Record<keyof RegistrationPayload, string>>
}


export function isRegistrationResponseError(error: unknown): error is RegistrationResponseError {
	return error != null
		&& typeof error == "object"
		&& "details" in error
}


export async function registrationFetch(registrationPayload: RegistrationPayload): Promise<User> {
	const response = await fetch("http://127.0.0.1:8000/auth/register", {
		method: "POST",
		body: JSON.stringify(registrationPayload),
		headers: { "Content-Type": "application/json" },
		credentials: "include"
	})
	const data = await response.json()

	if (!response.ok) {
		throw data
	}

	return data
}