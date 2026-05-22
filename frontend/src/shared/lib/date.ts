export function formatDateInput(input: string) {
	const digits = input.replace(/\D/g, "").slice(0, 8)

	if (digits.length <= 2)
		return digits
	if (digits.length <= 4) 
		return `${digits.slice(0, 2)}.${digits.slice(2)}`

	return `${digits.slice(0, 2)}.${digits.slice(2, 4)}.${digits.slice(4)}`
}

export function parseISOToDate(iso: string) {
	return iso.split("-").reverse().join(".")
}

export function parseDateToISO(date: string) { 
	return date.split(".").reverse().join("-")
}