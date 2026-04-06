import type { Ref } from "vue"
import { ref } from "vue"


export interface DataStore<T> {
	data: Ref<T | null>,
	error: Ref<string | null>,
	isPending:  Ref<boolean>
} 


export function useDataStore<T>(): DataStore<T> {
	const data = ref<T | null>(null) as Ref<T | null>
	const error = ref<string | null>(null)
	const isPending = ref(false)

	return { data, error, isPending }
}