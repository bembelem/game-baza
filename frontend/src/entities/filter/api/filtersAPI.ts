import type { SelectorValue } from "@/shared/interface/Filters"
import type { 
	FilterValue, 
	GenresFilter, 
	PlatformsFilter, 
	PublishersFilter, 
	StoresFilter 
} from "../model/Filter"


const toUIFilterValue = (filterValue: FilterValue): SelectorValue<string> => ({
	title: filterValue.name,
	value: filterValue.name
})

export async function getGenresFilterFetch(): Promise<SelectorValue<string>[]> {
	await new Promise(resolve => setTimeout(resolve, 2000))

	const response = await fetch("http://127.0.0.1:8000/genres", { method: "GET" })

	if (!response.ok) {
		throw new Error(`Ошибка getGenresFilterFetch: ${response.status}`) 
	}

	const data: GenresFilter = await response.json()

	return data.genres.map(toUIFilterValue)
}


export async function getPlatformsFilterFetch(): Promise<SelectorValue<string>[]> {
	await new Promise(resolve => setTimeout(resolve, 1500))

	const response = await fetch("http://127.0.0.1:8000/platforms", { method: "GET" })

	if (!response.ok) {
		throw new Error(`Ошибка getPlatformsFilterFetch: ${response.status}`) 
	}

	const data: PlatformsFilter = await response.json()

	return data.platforms.map(toUIFilterValue)
}


export async function getPublishersFilterFetch(): Promise<SelectorValue<string>[]> {
	await new Promise(resolve => setTimeout(resolve, 2500))

	const response = await fetch("http://127.0.0.1:8000/publishers", { method: "GET" })

	if (!response.ok) {
		throw new Error(`Ошибка getPublishersFilterFetch: ${response.status}`) 
	}

	const data: PublishersFilter = await response.json()

	return data.publishers.map(toUIFilterValue)
}


export async function getStoresFilterFetch(): Promise<SelectorValue<string>[]> {
	await new Promise(resolve => setTimeout(resolve, 3000))

	const response = await fetch("http://127.0.0.1:8000/stores", { method: "GET" })

	if (!response.ok) {
		throw new Error(`Ошибка getPublishersFilterFetch: ${response.status}`) 
	}

	const data: StoresFilter = await response.json()

	return data.stores.map(toUIFilterValue)
}