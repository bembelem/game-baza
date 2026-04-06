import type { User } from "../model/User"

// TODO: type guard для getIserFetch
// interface GetUserResponseError {
// 	summary: string,
// 	value: {
// 		error: string,
// 		message: string,
// 		details: Object,
// 		traceId: string
// 	}
// }


export async function getUserFetch(): Promise<User> {
	const response = await fetch("http://127.0.0.1:8000/users/me", { 
		method: "GET",
		credentials: "include"
	})
	const data = await response.json()

	if (!response.ok) {
		throw data
	}
	
	return data
}