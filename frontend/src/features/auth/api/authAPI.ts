export interface AuthPayload {
	email: string,
	password: string
}

export interface AuthResponse {
	access_token: string,
  	token_type: string
}

export interface AuthResponseError {
	details: Partial<Record<keyof AuthPayload, string>>
}


export function isAuthResponseError(error: unknown): error is AuthResponseError {
	return error != null
		&& typeof error == "object"
		&& "details" in error
}


export async function authFetch(authPayload: AuthPayload): Promise<AuthResponse> {
	await new Promise(resolve => setTimeout(resolve, 2000))

	const response = await fetch("http://127.0.0.1:8000/auth/login", { 
		method: "POST",
		body: JSON.stringify(authPayload) 
	})
	const data = await response.json()

	if (!response.ok) {
		throw data 
	}

	return data
}