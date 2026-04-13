import type { DataStore } from "./useDataStore"
import type { Ref } from "vue"


export async function fetchData<T>(
	dataStore: DataStore<T>, 
	fetchAPI: () => Promise<T>
) {
	dataStore.isPending.value = true
	try {
		dataStore.data.value = await fetchAPI()
	} catch (error) {
		dataStore.error.value = error instanceof Error 
			? error.message 
			: String(error)
	} finally {
		dataStore.isPending.value = false
	}
}


export const updateFetchDataController = (abortController: Ref<AbortController | undefined>) => {
	if (abortController.value) {
		console.log("fetchDataAbort")
		abortController.value.abort()
	}
	
	abortController.value = new AbortController()
	
	return abortController.value
}