import type { RegistrationFormFields } from "../ui/RegistartionForm.vue"
import type { RegistrationPayload } from "@/features/registration/api/registrationAPI"


export function toRegistrationPayload(fields: RegistrationFormFields): RegistrationPayload {
	fields.birthdate = fields.birthdate.split(".").reverse().join("-")
	
	return fields
}