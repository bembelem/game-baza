import { useField } from "vee-validate"
import { reactive } from "vue"


export function useFormField (name: string) {
	const {value, handleBlur, validate}  = useField<string>(name, undefined, {
		validateOnValueUpdate: false
	})
	
	return reactive({
		value,
		onBlur: () => {
			handleBlur()
			validate()
		}
	})
}