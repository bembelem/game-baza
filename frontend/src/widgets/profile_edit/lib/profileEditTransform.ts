import type { ProfileEditFormFields } from "../ui/ProfileEditForm.vue"
import type { ProfileEditPayload } from "@/features/profile_edit/api/profileEditAPI"
import { parseDateToISO } from "@/shared/lib/date"


export function toProfileEditPayload(fields: ProfileEditFormFields): ProfileEditPayload {
	const { newPassword, confirmPassword, ...profileEditPayload } = fields

	return { ...profileEditPayload, 
		birthdate: parseDateToISO(profileEditPayload.birthdate),
		password: newPassword  
	}
}