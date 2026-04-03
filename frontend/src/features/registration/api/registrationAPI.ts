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


export async function registrationFetch(registrationPayload: RegistrationPayload) {
	await new Promise(resolve => setTimeout(resolve, 2000))

	const response = await fetch("http://127.0.0.1:8000/auth/register", {
		method: "POST",
		body: JSON.stringify(registrationPayload)
	})

	if (!response.ok) {
		throw await response.json()
	}
}