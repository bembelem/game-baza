import { 
	type SelectorValue, 
	type FiltersDefinition,
	ResetBehavior 
} from "@/shared/interface/Filters"


export interface SearchGamesFilters {
 	sort: SelectorValue<string>,
 	price: SelectorValue<[number, number] | undefined>
 	genres: SelectorValue<string>[]
 	stores: SelectorValue<string>[]
}

type SearchGamesFiltersDefinition = FiltersDefinition<SearchGamesFilters>


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

export const priceValues: SelectorValue<[number, number] | undefined>[] = [
	{
		title: "все цены",
		value: undefined
	},
	{
		title: "до 1000₽", 
		value: [0, 1000]
	},
	{
		title: "1000-3000₽", 
		value: [1000, 3000]
	},
	{
		title: "3000-6000₽", 
		value: [3000, 6000]
	},
	{
		title: "от 6000₽", 
		value: [6000, 0]
	}
] 

export const searchGamesFiltersDefinition: SearchGamesFiltersDefinition = {
	sort: {
		values: sortValues,
		defaultValue: sortValues[0],
		resetBehavior: ResetBehavior.ToDefault
	},
	price: {
		values: priceValues,
		defaultValue: priceValues[0],
		resetBehavior: ResetBehavior.ToDefault
	},
	genres: {
		resetBehavior: ResetBehavior.Clear
	},
	stores: {
		resetBehavior: ResetBehavior.Clear
	},
}