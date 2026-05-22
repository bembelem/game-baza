import type { User } from "@/entities/user/model/User"


export interface ProfileEditPayload {
	username: string,
	email: string,
	password: string,
	birthdate: string,
}


export async function profileEditFetch(profileEditPayload: ProfileEditPayload): Promise<User> {
	const response = await fetch("http://localhost:8000/users/me", {
		method: "PATCH",
		body: JSON.stringify(profileEditPayload),
		headers: { "Content-Type": "application/json" },
		credentials: "include"
	})
	const data = await response.json()

	if (!response.ok) {
		throw data
	}

	return data
}