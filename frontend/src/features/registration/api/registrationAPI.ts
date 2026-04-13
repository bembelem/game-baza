import type { User } from "@/entities/user/model/User"
import type { APIValidationError } from "@/shared/interface/APIError"


export interface RegistrationPayload {
	username: string,
	email: string,
	password: string,
	birthdate: string
}

export type RegistrationResponseError = APIValidationError<Partial<RegistrationPayload>>


export async function registrationFetch(registrationPayload: RegistrationPayload): Promise<User> {
	const response = await fetch("http://localhost:8000/auth/register", {
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