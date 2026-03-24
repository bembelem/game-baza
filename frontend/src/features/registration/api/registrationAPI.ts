interface RegistrationPayload {
	email: string,
	password: string
}

interface RegistrationResponse {
	token: string
}


export async function registrationFetch(registrationPayload: RegistrationPayload): Promise<RegistrationResponse> {
	await new Promise(resolve => setTimeout(resolve, 2000))

	const response = await fetch("")

	if (!response.ok) {
		throw new Error(`registrationFetch error: ${response.status}`)
	}

	return await response.json()
}