interface AuthPayload {
	email: string,
	password: string
}

interface AuthResponse {
	token: string
}


export async function authFetch(authPayload: AuthPayload): Promise<AuthResponse> {
	await new Promise(resolve => setTimeout(resolve, 2000))

	const response = await fetch("")

	if (!response.ok) {
		throw new Error(`authFetch error: ${response.status}`)
	}

	return await response.json()
}