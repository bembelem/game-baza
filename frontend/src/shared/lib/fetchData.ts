import type { DataStore } from "./useDataStore"


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