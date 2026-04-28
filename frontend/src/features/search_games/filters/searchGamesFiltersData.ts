import type { SelectorValue } from "@/shared/interface/Filters"
import { useDataStore } from "@/shared/lib/useDataStore"


export const sortValues = [
	{
		title: "по популярности", 
		value: "popularity"
	},
	{
		title: "по рейтингу", 
		value: "rating"
	},
	{
		title: "сначала дешевые", 
		value: "cheap"
	},
	{
		title: "сначала дорогие", 
		value: "expensive"
	},
	{
		title: "по скидке", 
		value: "sale"
	},
	{
		title: "по дате выхода", 
		value: "release_date"
	},
	{
		title: "по дате добавления", 
		value: "addition_date"
	},
	{
		title: "по алфавиту", 
		value: "alphabet"
	}
]


export const genresFilterOptions = useDataStore<SelectorValue<string>[]>()
export const platformsFilterOptions = useDataStore<SelectorValue<string>[]>()
export const publishersFilterOptions = useDataStore<SelectorValue<string>[]>()
export const storesFilterOptions = useDataStore<SelectorValue<string>[]>()


export const availableSearchGamesFiltersOptions = {
	genres: genresFilterOptions.data,
	publishers: publishersFilterOptions.data
}