import type { RegistrationFormFields } from "../ui/RegistartionForm.vue"
import type { RegistrationPayload } from "@/features/registration/api/registrationAPI"
import { parseDateToISO } from "@/shared/lib/date"


export function toRegistrationPayload(fields: RegistrationFormFields): RegistrationPayload {
	fields.birthdate = parseDateToISO(fields.birthdate)
	
	return fields
}