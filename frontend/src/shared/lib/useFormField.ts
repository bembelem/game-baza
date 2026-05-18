import { useField } from "vee-validate"


export function useFormField (name: string) {
	const {value, handleBlur, validate}  = useField<string>(name, undefined, {
		validateOnValueUpdate: false
	})
	
	return {
		value,
		onBlur: () => {
			handleBlur()
			validate()
		}
	}
}