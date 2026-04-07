export interface APIValidationError<T extends Record<string, string> = Record<string, string>> {
	error: string
	message: string
	details: T
	traceId: string
}


export function isAPIValidationError(error: unknown): error is APIValidationError {
	return error !== null 
		&& typeof error === "object"  
		&& "error" in error 
		&& "details" in error
		&& "traceId" in error
}