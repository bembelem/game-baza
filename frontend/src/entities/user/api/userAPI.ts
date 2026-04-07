import type { User } from "../model/User"


export async function getUserFetch(): Promise<User> {
	const response = await fetch("http://localhost:8000/users/me", { 
		method: "GET",
		credentials: "include"
	})
	const data = await response.json()

	if (!response.ok) {
		throw data
	}
	
	return data
}